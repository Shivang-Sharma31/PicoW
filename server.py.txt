from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

led_state = "OFF"  # global LED state

@app.route('/')
def index():
    return render_template('index.html', state=led_state)

@socketio.on('toggle_led')
def handle_led_toggle(data):
    global led_state
    led_state = data['state']
    print(f"LED set to {led_state}")
    emit('led_state', {'state': led_state}, broadcast=True)

@socketio.on('get_led_state')
def handle_get_led_state():
    emit('led_state', {'state': led_state})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
