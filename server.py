from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('led')
def handle_led(data):
    print(f"LED command: {data}")
    # Later, forward this command to Pico W using MQTT or direct WebSocket
    emit('led_status', f"LED turned {data}", broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
