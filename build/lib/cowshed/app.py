import json
import os

from flask import Flask, abort, jsonify, request

app = Flask(__name__)

DATA_FILE = 'cows.json'

def read_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def write_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/cows', methods=['GET'])
def get_cows():
    cows = read_data()
    sex = request.args.get('sex')
    if sex:
        cows = [cow for cow in cows if cow['sex'].lower() == sex.lower()]
    return jsonify(cows)

@app.route('/cows/<name>', methods=['GET'])
def get_cow(name):
    cows = read_data()
    cow = next((cow for cow in cows if cow['name'] == name), None)
    if cow is None:
        abort(404)
    return jsonify(cow)

@app.route('/cows', methods=['POST'])
def create_cow():
    if not request.json or not 'name' in request.json:
        abort(400, description="Invalid JSON or missing 'name'")
    new_cow = {
        'name': request.json['name'],
        'sex': request.json.get('sex', ""),
        'birthdate': request.json.get('birthdate', ""),
        'condition': request.json.get('condition', ""),
        'weight': request.json.get('weight', {}),
        'feeding': request.json.get('feeding', {}),
        'milk_production': request.json.get('milk_production', {}),
        'has_calves': request.json.get('has_calves', False)
    }
    cows = read_data()
    if any(cow['name'] == new_cow['name'] for cow in cows):
        abort(400, description="Cow with this name already exists")
    cows.append(new_cow)
    write_data(cows)
    return jsonify(new_cow), 201

@app.route('/cows/<name>', methods=['PUT'])
def update_cow(name):
    cows = read_data()
    cow = next((cow for cow in cows if cow['name'] == name), None)
    if cow is None:
        abort(404)
    if not request.json:
        abort(400)
    cow.update({
        'sex': request.json.get('sex', cow['sex']),
        'birthdate': request.json.get('birthdate', cow['birthdate']),
        'condition': request.json.get('condition', cow['condition']),
        'weight': request.json.get('weight', cow['weight']),
        'feeding': request.json.get('feeding', cow['feeding']),
        'milk_production': request.json.get('milk_production', cow['milk_production']),
        'has_calves': request.json.get('has_calves', cow['has_calves'])
    })
    write_data(cows)
    return jsonify(cow)

@app.route('/cows/<name>', methods=['DELETE'])
def delete_cow(name):
    cows = read_data()
    cow = next((cow for cow in cows if cow['name'] == name), None)
    if cow is None:
        abort(404)
    cows.remove(cow)
    write_data(cows)
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
