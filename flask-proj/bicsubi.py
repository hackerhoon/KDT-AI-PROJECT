from flask import Flask, jsonify, request
import sqlite3
import requests

app = Flask(__name__)

db = "weapon.db"



def init_db(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS weapons (
            name TEXT NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

whoami = "mygithubid"
init_db(db)
@app.route('/')#해당주소가 요청받았을때 밑의 함수를 실행

def hello():
    return "Hello"

# whoami
@app.route('/whoami')
def get_whoami():
    return jsonify({"name": whoami})

# GET /echo?string="string"
@app.route('/echo')
def get_echo():
    request_data = request.args.get('string')
    return jsonify({'value' : request_data})

@app.route('/weapon')
def read_weapons():
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT * FROM weapons")
        weapons = c.fetchall()
        return jsonify({"weapons":weapons})
    finally:
        conn.close()

@app.route('/weapon', methods=['POST'])
def create_weapon():
    request_data = request.get_json()
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("""
            INSERT INTO weapons (name, stock)
            VALUES (?, ?)
        """, (request_data['name'], request_data['stock']))
        conn.commit()
        return jsonify({'name': request_data['name'], "stock": request_data['stock']})
    finally:
        conn.close()

@app.route('/weapon/<string:name>', methods=['PUT'])
def update_weapon(name):
    request_data = request.get_json()
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT * FROM weapons WHERE name=?", (name,))
        weapon = c.fetchone()

        if weapon is None:
            return f'{404} Error: Weapon not found'

        c.execute("""
            UPDATE weapons SET name = ?, stock = ? WHERE name = ?
        """, (request_data['name'], request_data['stock'], name))
        conn.commit()

        return jsonify({'name':request_data['name'], 'stock':request_data['stock']})
    finally:
        conn.close()

@app.route('/weapon/<string:name>', methods=['DELETE'])
def delete_data(name):
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT * FROM weapons WHERE name=?", (name,))
        weapon = c.fetchone()
        if weapon is None:
            return f'{404} Error: Weapon not found'

        c.execute("DELETE FROM weapons where name = ?", (name,))
        conn.commit()
        return jsonify({'name': weapon[0], 'stock':weapon[1]})
    finally:
        conn.close()


with open('apikey','r') as f:
    api_key = f.read()

@app.route('/weather')
def get_weather():

    request_data = request.get_json() # 별도의 위도 경도를 입력해야됨 -> GEOLOCATION을 사용하면 추가적으로 구현이 가능하나 API발급이 또 필요함
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={request_data["lat"]}&lon={request_data["lon"]}&appid={api_key}&units=Metric'
    
    res = requests.get(url)
    if res.status_code != 200:
        return f'{res.status_code} Error: Failed to get weather infomation'
    weather_data = res.json()
    return jsonify({'temperature': weather_data['main']['temp'],'wind_speed': weather_data['wind']['speed']})

if __name__ == '__main__':
    app.run()