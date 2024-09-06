from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins for simplicity

# In-memory notification store (for demonstration purposes)
notifications = []

@app.route('/')
def index():
    return render_template('index_Q13.html')

@app.route('/send_update')
def send_update():
    # Simulate a new update
    notification = {
        'message': 'New update at {}'.format(time.strftime('%Y-%m-%d %H:%M:%S'))
    }
    notifications.append(notification)
    socketio.emit('notification', notification, broadcast=True)
    return 'Update sent!'

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    # Send the current notifications to the newly connected client
    emit('notification_list', notifications)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
