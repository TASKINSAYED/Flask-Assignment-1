from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database setup
DATABASE = 'users.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# User model
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    user_row = db.execute('SELECT id, username, password_hash FROM users WHERE id = ?', (user_id,)).fetchone()
    if user_row:
        return User(user_row['id'], user_row['username'], user_row['password_hash'])
    return None

@app.route('/')
@login_required
def home():
    return render_template('home_Q8.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user_row = db.execute('SELECT id, username, password_hash FROM users WHERE username = ?', (username,)).fetchone()
        if user_row and check_password_hash(user_row['password_hash'], password):
            user = User(user_row['id'], user_row['username'], user_row['password_hash'])
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)
        db = get_db()
        db.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
        db.commit()
        return redirect(url_for('login'))
    return render_template('register_Q8.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host="0.0.0.0")

import sqlite3

def init_db():
    with open('schema.sql', 'r') as f:
        conn = sqlite3.connect('users.db')
        conn.executescript(f.read())
        conn.close()

if __name__ == '__main__':
    init_db()
