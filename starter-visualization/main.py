# Import the Quix Streams modules for interacting with Kafka:
from quixstreams import Application
# (see https://quix.io/docs/quix-streams/v2-0-latest/api-reference/quixstreams.html for more details)

# Import additional modules as needed
import os
import threading

from flask import Flask, render_template
from flask_socketio import SocketIO

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

def run_socketio_app():
    socketio.run(app, host='0.0.0.0', port=80, debug=True)

def send_telemetry(data: dict):
    socketio.emit('telemetry', data)

if __name__ == '__main__':
    # Start the SocketIO server in a separate thread
    thread = threading.Thread(target=run_socketio_app)
    thread.start()

    load_dotenv(override=False)

    # Create an Application.
    quix_app = Application()

    input_topic = quix_app.topic(os.environ["input"])

    sdf = quix_app.dataframe(input_topic)
    sdf = sdf.update(send_telemetry)
    sdf = sdf.print()

    quix_app.run(sdf)