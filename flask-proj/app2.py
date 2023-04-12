from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DB_NAME = "menus.db"

def initialize_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS menus (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price INTEGER NOT NULL
        );
    """)
    conn.commit()
    conn.close()

initialize_db()

@app.route('/')
def hello_flask():
    return "Hello World!"

@app.route('/menus')
def get_menus():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM menus")
    menus = c.fetchall()
    conn.close()
    return jsonify({"menus": menus})

@app.route('/menus', methods=['POST'])
def create_menu():
    request_data = request.get_json()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO menus (name, price)
        VALUES (?, ?)
    """, (request_data['name'], request_data['price']))
    conn.commit()
    new_menu_id = c.lastrowid
    conn.close()
    return jsonify({"id": new_menu_id, "name": request_data['name'], "price": request_data['price']})

@app.route('/menus/<int:id>', methods=['PUT'])
def update_data(id):
    request_data = request.get_json()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        UPDATE menus SET name = ?, price = ? WHERE id = ?
    """, (request_data['name'], request_data['price'], id))
    conn.commit()
    if c.rowcount == 0:
        return f"ID {id} doesn't exist. Fail to update."
    conn.close()
    return jsonify({"id": id, "name": request_data['name'], "price": request_data['price']})

@app.route('/menus/<int:id>', methods=['DELETE'])
def delete_data(id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        DELETE FROM menus WHERE id = ?
    """, (id,))
    conn.commit()
    if c.rowcount == 0:
        return f"ID {id} doesn't exist. Fail to delete."
    conn.close()
    return f"ID {id} deleted successfully."


if __name__ == '__main__':
    app.run()