from flask import Flask
from flask_socketio import SocketIO, emit
import eventlet

# Monkey patch must be the VERY first thing
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# UPDATE THIS LINE:
# 1. async_mode='eventlet' (Crucial for Render)
# 2. max_http_buffer_size=10000000 (Allows 10MB frames, prevents disconnects)
# 3. ping_timeout=60 (More tolerant of slow internet)
socketio = SocketIO(app, 
                    cors_allowed_origins="*", 
                    async_mode='eventlet', 
                    max_http_buffer_size=10000000, 
                    ping_timeout=60)

@app.route('/')
def index():
    return "Video Relay Server is Online."

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('video_frame_from_laptop')
def handle_frame(data):
    emit('new_frame_for_viewers', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
