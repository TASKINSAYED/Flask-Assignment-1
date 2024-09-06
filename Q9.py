from flask import Flask, request, jsonify, abort
import sqlite3

app = Flask(__name__)

# Database setup
DATABASE = 'books.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        with open('schema_Q9.sql', mode='r') as f:
            db.executescript(f.read())

@app.before_first_request
def initialize_database():
    init_db()

# Routes for CRUD operations

@app.route('/books', methods=['GET'])
def get_books():
    db = get_db()
    cur = db.execute('SELECT id, title, author, year FROM books')
    books = cur.fetchall()
    return jsonify([dict(book) for book in books])

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    db = get_db()
    cur = db.execute('SELECT id, title, author, year FROM books WHERE id = ?', (book_id,))
    book = cur.fetchone()
    if book is None:
        abort(404)
    return jsonify(dict(book))

@app.route('/books', methods=['POST'])
def create_book():
    if not request.json or not all(k in request.json for k in ('title', 'author', 'year')):
        abort(400)
    title = request.json['title']
    author = request.json['author']
    year = request.json['year']
    db = get_db()
    cur = db.execute('INSERT INTO books (title, author, year) VALUES (?, ?, ?)', (title, author, year))
    db.commit()
    book_id = cur.lastrowid
    return jsonify({'id': book_id, 'title': title, 'author': author, 'year': year}), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    if not request.json or not all(k in request.json for k in ('title', 'author', 'year')):
        abort(400)
    title = request.json['title']
    author = request.json['author']
    year = request.json['year']
    db = get_db()
    cur = db.execute('UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?', (title, author, year, book_id))
    db.commit()
    if cur.rowcount == 0:
        abort(404)
    return jsonify({'id': book_id, 'title': title, 'author': author, 'year': year})

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    db = get_db()
    cur = db.execute('DELETE FROM books WHERE id = ?', (book_id,))
    db.commit()
    if cur.rowcount == 0:
        abort(404)
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(host="0.0.0.0")
