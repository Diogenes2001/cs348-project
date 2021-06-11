import json
from flask import Flask, request, json, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, InfoModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost:5432/Flask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# FORMAT:
# Array of arrays where each nested array has 3 or less pokemon
# e.g. POKEMON = [[Pokemon1, Pokemon2, Pokemon3],
#                 [Pokemon4, Pokemon5, Pokemon6],
#                 [Pokemon7, Pokemon8, Pokemon9]]
# Each nested array represents a row in the front-end
# Done this way so logic is easier for front-end
POKEMON = [
    [{
        'id': 1,
        'name': 'Bulbasaur',
        'types': ('Grass', 'Poison'),
        'hp': 1,
        'spd': 1,
        'atk': 1,
        'def': 2,
        'spAtk': 2,
        'spDef': 2,
    },
    {
        'id': 2,
        'name': 'Ivysaur',
        'types': ('Grass', 'Poison'),
        'hp': 1,
        'spd': 1,
        'atk': 1,
        'def': 2,
        'spAtk': 2,
        'spDef': 2,
    },
    {
        'id': 3,
        'name': 'Venusaur',
        'types': ('Grass', 'Poison'),
        'hp': 1,
        'spd': 1,
        'atk': 1,
        'def': 2,
        'spAtk': 2,
        'spDef': 2,
    }],
    [{
        'id': 4,
        'name': 'Charmander',
        'types': ('Fire',),
        'hp': 1,
        'spd': 1,
        'atk': 1,
        'def': 2,
        'spAtk': 2,
        'spDef': 2,
    },
    {
        'id': 5,
        'name': 'Charmeleon',
        'types': ('Fire',),
        'hp': 1,
        'spd': 1,
        'atk': 1,
        'def': 2,
        'spAtk': 2,
        'spDef': 2,
    },
    {
        'id': 6,
        'name': 'Charizard',
        'types': ('Fire',),
        'hp': 1,
        'spd': 1,
        'atk': 1,
        'def': 2,
        'spAtk': 2,
        'spDef': 2,
    }],
]

@app.route('/pokedex', methods=['POST'])
def all_pokemon():
    data = request.get_json()
    name = data['name']    # Name of pokemon user would like to filter for (empty means ALL)
    types = data['types']  # List of types user would like to filter for (empty means ALL)

    # TO-DO: Get from database and transform to proper format for front-end

    return jsonify({
        'status': 'success',
        'pokemon': POKEMON,
    })

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route("/test")
def test():
    new_user = InfoModel(name='Cinna', age='1')
    db.session.add(new_user)
    db.session.commit()
    return jsonify("Success!")

if __name__ == "main":
    app.run()