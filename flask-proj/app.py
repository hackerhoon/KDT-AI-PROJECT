from flask import Flask, jsonify, request

app = Flask(__name__)

menus = [
    {"id": 1, "name":"Espresso", "price":3800},
    {"id": 2, "name":"Americano", "price":4100},
    {"id": 3, "name":"CafeLatte", "price":4600},
]

@app.route('/')#해당주소가 요청받았을때 밑의 함수를 실행

def hello_flask():
    return "Hello World!"

# GET /menus : 자료를 가지고 온다.
@app.route('/menus')
def get_menus():
    return jsonify({"menus": menus})

# POST /menus : 자료를 자원에 추가한다.
@app.route('/menus', methods=['POST']) #defalut값으로 GET으로 설정되어 있음
def create_menu(): #request가 JSON이라고 가정
    # 전달받은 자료를 menus 자원에 추가
    request_data = request.get_json() # {"name": ... , "price": ...}
    new_menu = {
        'id':len(menus)+1,
        'name': request_data['name'],
        'price':request_data['price'],
    }
    menus.append(new_menu)
    return jsonify(new_menu)

@app.route('/menus/<int:id>', methods=['PUT'])
def update_data(id):
    request_data = request.get_json()
    for menu in menus:
        if menu['id'] == id:
            menu['name'] = request_data['name']
            menu['price'] = request_data['price'] 
            return jsonify(menu)
    return f"ID isn't exist. Fail to update {id}"

@app.route('/menus/<int:id>', methods=['DELETE'])
def delete_data(id):
    request_data = request.get_json()
    for menu in menus:
        if menu['id'] == id:
            del_menu = menu
            menus.remove(menu)
            return f"[DELETE]: {del_menu}"
    return f"ID isn't exist. Fail to delete {id}"

if __name__ == '__main__':
    app.run()