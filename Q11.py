from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins for simplicity

@app.route('/')
def index():
    return render_template('index_Q11.html')

@socketio.on('message')
def handle_message(message):
    print(f'Received message: {message}')
    emit('response', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")
