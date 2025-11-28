from flask import Flask
from flask_socketio import SocketIO, emit
import eventlet

# Necessary for Render deployment
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# Allow connection from anywhere (*)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/')
def index():
    return "Video Relay Server is Online."

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('video_frame_from_laptop')
def handle_frame(data):
    # Broadcast the received frame to all viewers
    emit('new_frame_for_viewers', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
