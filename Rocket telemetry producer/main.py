import datetime
import quixstreams as qx
import time
import pandas as pd
import os

from dotenv import load_dotenv

load_dotenv()

# Quix injects credentials automatically to the client.
# Alternatively, you can always pass an SDK token manually as an argument.
client = qx.QuixStreamingClient()

# Open the output topic
print("Opening output topic")
producer_topic = client.get_topic_producer(os.environ["output"])

# Create a new stream_producer. A stream is a collection of data that belong to a single session of a single source.
# For example single car journey.
# If you don't specify a stream id, a random guid is used.
stream_producer = producer_topic.create_stream()

# If you want append data into the stream later, assign a stream id.
# stream = producer_topic.create_stream("my-own-stream-id")

# Give the stream human readable name. This name will appear in data catalogue.
stream_producer.properties.name = "rocket telemetry"

# Add stream metadata to add context to time series data.
stream_producer.properties.metadata["rocket"] = os.environ["rocket"]

# Read the CSV data
folder_name = "{}/JSON STREAMING".format(os.environ["rocket"])
file_name1 = '{} raw.json'.format(os.environ["rocket"])
file_name2 = 'analysed.json'

# Create the full file paths
file_path1 = os.path.join('.', folder_name, file_name1)
file_path2 = os.path.join('.', folder_name, file_name2)

# Read the JSON data into Pandas DataFrames
df1 = pd.read_json(file_path1, lines=True)
df2 = pd.read_json(file_path2, lines=True)

df2 = df2.drop(columns=["velocity", "altitude"])

# Convert the "time" column to nanoseconds in both DataFrames
df1['time'] = (df1['time'] * 1e9).astype('int64')
df2['time'] = (df2['time'] * 1e9).astype('int64')

# Merge the DataFrames based on "time" column
merged_df = pd.merge_asof(df1, df2, on="time")

# Fill in missing properties using fillna with the method='ffill' (forward fill)
df = merged_df.fillna(method='ffill')

# Add optional metadata to parameters.
stream_producer.epoch = datetime.datetime.utcnow()

stream_producer.timeseries.add_definition("velocity", "Velocity").set_unit("KMH")
stream_producer.timeseries.add_definition("altitude", "Altitude").set_unit("KM")
stream_producer.timeseries.add_definition("velocity_x", "Velocity_X").set_unit("KMH")
stream_producer.timeseries.add_definition("velocity_y", "Velocity_Y").set_unit("KMH")
stream_producer.timeseries.add_definition("acceleration", "Acceleration").set_unit("KMS2")
stream_producer.timeseries.add_definition("angle", "Angle").set_unit("degrees")

# Every second we read one second worth of data from data frame and send it to the platform.
print("Writing data")
df['time'] = pd.to_datetime(df['time'], unit='ns', utc=True)

start_loop = time.time()
first_time = df['time'].iloc[0]

for i in range(len(df)):
    df_i = df.iloc[[i]]

    # Calculate the time difference between consecutive rows
    time_diff = (df['time'].iloc[i] - first_time).total_seconds()

    stream_producer.timeseries.publish(df_i)
    #print("Sending " + str(i) + "/" + str(len(df)))
    print(df_i)

    time_to_wait = max(0.0, time_diff - (time.time() - start_loop))
    time.sleep(time_to_wait)

print("Closing stream")

# Stream can be infinitely long or have start and end.
# If you send data into closed stream, it is automatically opened again.
stream_producer.close()