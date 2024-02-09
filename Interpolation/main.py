import os
from quixstreams import Application, State, message_context
from quixstreams.models.serializers.quix import QuixDeserializer, QuixTimeseriesSerializer
import uuid

app = Application.Quix(str(uuid.uuid4()), auto_offset_reset="latest")

input_topic = app.topic(os.environ["input"], value_deserializer=QuixDeserializer())
output_topic = app.topic(os.environ["output"], value_serializer=QuixTimeseriesSerializer())

sdf = app.dataframe(input_topic)

def join_data(row: dict, state: State):
    
    join_state = state.get("join_state", {
        "left_outer_values": []
    })

    if os.environ["output"] in row:
        if "right_values" not in join_state:
            print("Once")
            join_state["right_values"] = row
            state.set("join_state", join_state)
            return []
        else:
            values_to_return = []
            for i in range(0, len(join_state["left_outer_values"])-1):
                right_interpolated = {}
                for key in join_state["right_values"]:
                    if key == "Timestamp" or key == "Tags":
                        continue

                    delta = row[key] - join_state["right_values"][key]
                    step = delta / (len(join_state["left_outer_values"]) + 1)
                    right_interpolated[key] = join_state["right_values"][key] + (step*(i+1))
                    join_state["left_outer_values"][i] = {**join_state["left_outer_values"][i], **right_interpolated}
                    
                values_to_return.append(join_state["left_outer_values"][i])
                i+=1

            join_state["right_values"] = row    
            join_state["left_outer_values"] = []
            state.set("join_state", join_state)

            return values_to_return
    else:
        join_state["left_outer_values"].append(row)
        state.set("join_state", join_state)

        return []


sdf = sdf.apply(join_data, stateful=True, expand=True)

sdf = sdf.update(lambda row: print(str(message_context().offset) +str(list(row.values()))))

sdf = sdf.to_topic(output_topic)

if __name__ == "__main__":
    app.run(sdf)