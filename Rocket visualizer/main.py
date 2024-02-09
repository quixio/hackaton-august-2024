import uuid
import os
import threading

from flask import Flask, render_template
from flask_socketio import SocketIO

from quixstreams import Application, State
from quixstreams.models.serializers.quix import QuixSerializer, JSONSerializer, QuixDeserializer, JSONDeserializer
# import the dotenv module to load environment variables from a file
from dotenv import load_dotenv

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*', async_mode="threading")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# Simulating rocket telemetry updates (replace this with your logic)
def simulate_telemetry():
    import time
    import random

def run_socketio_app():
    socketio.run(app)

def send_telemetry(data: dict):

    telemetry = {
        'x': data["X"],
        'y': data["Y"],
        'angle': data["angle"] * -1,
        'velocity': data["velocity"],
        'velocity_x': data["velocity_x"],
        'velocity_y': data["velocity_y"],
        'acceleration': data["acceleration"],
        'altitude': data["altitude"]
    }

    socketio.emit('telemetry', telemetry)

def run_socketio_app():
    socketio.run(app)

if __name__ == '__main__':
    # Start the SocketIO server in a separate thread
    thread = threading.Thread(target=run_socketio_app)
    thread.start()

    load_dotenv(override=False)

    quix_app = Application.Quix(

        consumer_group=str(uuid.uuid4()),
        auto_offset_reset="latest",
        auto_create_topics=True,  # Quix app has an option to auto create topics
    )

    input_topic = quix_app.topic(os.environ["input"], value_deserializer=JSONDeserializer())

    sdf = quix_app.dataframe(input_topic)

    sdf = sdf.update(lambda row: print(row))

    sdf = sdf.update(send_telemetry)
    quix_app.run(sdf)