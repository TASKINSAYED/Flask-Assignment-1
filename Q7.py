from flask import Flask, request, jsonify, abort
import sqlite3

app = Flask(__name__)

# Database setup
DATABASE = 'items.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        with open('schema_Q7.sql', mode='r') as f:
            db.executescript(f.read())

@app.before_first_request
def initialize_database():
    init_db()

# Routes for CRUD operations

@app.route('/items', methods=['GET'])
def get_items():
    db = get_db()
    cur = db.execute('SELECT id, name FROM items')
    items = cur.fetchall()
    return jsonify([dict(item) for item in items])

@app.route('/item/<int:item_id>', methods=['GET'])
def get_item(item_id):
    db = get_db()
    cur = db.execute('SELECT id, name FROM items WHERE id = ?', (item_id,))
    item = cur.fetchone()
    if item is None:
        abort(404)
    return jsonify(dict(item))

@app.route('/item', methods=['POST'])
def create_item():
    if not request.json or not 'name' in request.json:
        abort(400)
    name = request.json['name']
    db = get_db()
    cur = db.execute('INSERT INTO items (name) VALUES (?)', (name,))
    db.commit()
    item_id = cur.lastrowid
    return jsonify({'id': item_id, 'name': name}), 201

@app.route('/item/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    if not request.json or not 'name' in request.json:
        abort(400)
    name = request.json['name']
    db = get_db()
    cur = db.execute('UPDATE items SET name = ? WHERE id = ?', (name, item_id))
    db.commit()
    if cur.rowcount == 0:
        abort(404)
    return jsonify({'id': item_id, 'name': name})

@app.route('/item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    db = get_db()
    cur = db.execute('DELETE FROM items WHERE id = ?', (item_id,))
    db.commit()
    if cur.rowcount == 0:
        abort(404)
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(host="0.0.0.0")
