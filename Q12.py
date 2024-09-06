from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins for simplicity

# In-memory data store (for demonstration purposes)
data_store = {'value': 0}

@app.route('/')
def index():
    return render_template('index_Q12.html')

@socketio.on('update_data')
def handle_update_data(new_value):
    global data_store
    data_store['value'] = new_value
    emit('data_update', {'value': data_store['value']}, broadcast=True)

@socketio.on('get_data')
def handle_get_data():
    emit('data_update', {'value': data_store['value']})

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")
