import json
import os

from flask import Flask, abort, jsonify, request
from pydantic import BaseModel, Field, ValidationError, validator

app = Flask(__name__)

DATA_FILE = 'cows.json'

class Weight(BaseModel):
    mass_kg: float
    last_measured: str

class Feeding(BaseModel):
    amount_kg: float
    cron_schedule: str
    last_measured: str

class MilkProduction(BaseModel):
    last_milk: str
    cron_schedule: str
    amount_l: float

class Cow(BaseModel):
    name: str
    sex: str
    birthdate: str = ""
    condition: str = ""
    weight: Weight = Weight(mass_kg=0.0, last_measured="")
    feeding: Feeding = Feeding(amount_kg=0.0, cron_schedule="", last_measured="")
    milk_production: MilkProduction = MilkProduction(last_milk="", cron_schedule="", amount_l=0.0)
    has_calves: bool = False

    @validator('sex')
    def validate_sex(cls, value):
        if value.lower() not in ['male', 'female']:
            raise ValueError("Sex must be 'Male' or 'Female'")
        return value

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
    return jsonify(cows)

@app.route('/cows/<name>', methods=['GET'])
def get_cow(name):
    cows = read_data()
    cow = next((cow for cow in cows if cow['name'] == name), None)
    if cow is None:
        abort(404)
    return jsonify(cow)

@app.route('/cows/sex/<sex>', methods=['GET'])
def get_sex(sex):
    cows = read_data()
    filtered_cows = [cow for cow in cows if cow['sex'].lower() == sex.lower()]
    if not filtered_cows:
        abort(404)
    return jsonify(filtered_cows)

@app.route('/cows', methods=['POST'])
def create_cow():
    try:
        cow_data = request.get_json()
        cow = Cow(**cow_data)
    except ValidationError as e:
        abort(400, description=str(e))

    cows = read_data()
    if any(c['name'] == cow.name for c in cows):
        abort(400, description=f"Cow with name '{cow.name}' already exists")

    cows.append(cow.dict())
    write_data(cows)
    return jsonify(cow.dict()), 201

@app.route('/cows/<name>', methods=['PUT'])
def update_cow(name):
    cows = read_data()
    cow = next((c for c in cows if c['name'] == name), None)
    if cow is None:
        abort(404)

    try:
        cow_data = request.get_json()
        updated_cow = Cow(**cow_data)
    except ValidationError as e:
        abort(400, description=str(e))

    cow.update(updated_cow.dict())
    write_data(cows)
    return jsonify(updated_cow.dict())

@app.route('/cows/<name>', methods=['DELETE'])
def delete_cow(name):
    cows = read_data()
    cow = next((c for c in cows if c['name'] == name), None)
    if cow is None:
        abort(404)

    cows.remove(cow)
    write_data(cows)
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
