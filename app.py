from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
    {
        'name': 'Zdroweda',
        'items': [
            {'name': 'Candles', 'price': 54.99},
            {'name': 'Herbs', 'price': 5.99},
            {'name': 'Workshops', 'price': 599},
            {'name': 'Music teraphy', 'price': 45}
        ]
    },
    {
        'name': 'Skyzen',
        'items': [
            {'name': 'Trip', 'price': 5400},
            {'name': 'Photo session', 'price': 100},
            {'name': 'Workshops', 'price': 200}
        ]
    }
]


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


# In backend we use:
# POST - For reveiving data
# GET - for sending data


# %%% Creating endpoints %%%

@app.route("/store", methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


@app.route('/store/<string:name>', methods=['GET'])
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store) # Remember to always jsonify your data
    return jsonify({'message': 'Store not found'})


@app.route("/store")
def get_stores():
    return jsonify({'stores': stores})


@app.route("/store/<string:name>/item", methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()

    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'Store not found'})



@app.route("/store/<string:name>/item")
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})  # Remember to always jsonify your data
    return jsonify({'message': 'Store not found'})


if __name__ == '__main__':
    app.run(port=5000)
