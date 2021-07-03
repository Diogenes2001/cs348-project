import json
from flask import Flask, request, json, jsonify
from flask_cors import CORS
import psycopg2
import sys

app = Flask(__name__)

# connect to the database
conn = psycopg2.connect(host="localhost",
    database="Flask", user="postgres", password="password")
cur = conn.cursor()

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

def get_color_by_type(type):
    if type == 'Normal':
        return '#a8a888'
    elif type == 'Fire':
        return '#f08437'
    elif type == 'Water':
        return '#6e95f0'
    elif type == 'Grass':
        return '#84c763'
    elif type == 'Electric':
        return '#f7d034'
    elif type == 'Ice':
        return '#a0d9d9'
    elif type == 'Fighting':
        return '#bf4943'
    elif type == 'Poison':
        return '#a15fa1'
    elif type == 'Ground':
        return '#e0c375'
    elif type == 'Flying':
        return '#ac95f0'
    elif type == 'Psychic':
        return '#f75c8a'
    elif type == 'Bug':
        return '#acb83e'
    elif type == 'Rock':
        return '#b8a654'
    elif type == 'Ghost':
        return '#7f7099'
    elif type == 'Dark':
        return '#70655e'
    elif type == 'Dragon':
        return '#743bf7'
    elif type == 'Steel':
        return '#bebed1'
    else:  # type == 'Fairy'
        return '#f0b9be'

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
        'colors': (get_color_by_type('Grass'),get_color_by_type('Poison')),
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
        'colors': (get_color_by_type('Grass'),get_color_by_type('Poison')),
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
        'colors': (get_color_by_type('Grass'),get_color_by_type('Poison')),
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
        'colors': (get_color_by_type('Fire'),),
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
        'colors': (get_color_by_type('Fire'),),
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
        'colors': (get_color_by_type('Fire'),),
        'hp': 1,
        'spd': 1,
        'atk': 1,
        'def': 2,
        'spAtk': 2,
        'spDef': 2,
    }],
]

@app.route('/deleteaccount', methods=['POST'])
def try_deleteaccount():
    data = request.get_json()

    cur.execute('''SELECT password FROM "User" WHERE username='{0}' '''.format(data['username']))

    tup = cur.fetchone()
    if tup is not None:
        passw = tup[0]

        if passw == data['password']:

            cur.execute('''DELETE FROM "User" WHERE username='{0}' '''.format(data['username']))

            conn.commit()

            return jsonify({'status': 'success', 'error': 'Successfully deleted your account.'})

    return jsonify({'status': 'failure', 'error': 'The password was incorrect.'})

@app.route('/changepass', methods=['POST'])
def try_changepass():
    data = request.get_json()

    cur.execute('''SELECT password FROM "User" WHERE username='{0}' '''.format(data['username']))

    tup = cur.fetchone()
    if tup is not None:
        passw = tup[0]

        if passw == data['curpass']:

            cur.execute('''UPDATE "User" SET password = '{0}' WHERE username='{1}' '''.format(data['newpass'], data['username']))

            conn.commit()

            return jsonify({'status': 'success', 'error': 'Successfully updated your password.'})

    return jsonify({'status': 'failure', 'error': 'Current password was incorrect.'})

@app.route('/signup', methods=['POST'])
def try_signup():
    data = request.get_json()

    cur.execute('''SELECT * FROM "User" WHERE username='{0}' '''.format(data['username']))

    tup = cur.fetchone()
    if tup is not None:
        return jsonify({ 'status': 'failure', 'error': 'Username is already taken.'})
    
    cur.execute('''INSERT INTO "User" VALUES ('{0}', '{1}', '{2}') '''.format(data['username'], data['email'], data['password']))

    conn.commit()

    return jsonify({
        'status': 'success'
    })

@app.route('/login', methods=['POST'])
def try_login():
    data = request.get_json()

    cur.execute('''SELECT password FROM "User" WHERE username='{0}' '''.format(data['username']))

    tup = cur.fetchone()
    if tup is not None:
        passw = tup[0]

        if passw == data['password']:
            return jsonify({
                'status': 'success'
            })

    return jsonify({ 'status': 'failure', 'error': 'Username or password is incorrect.'})

# This route is for feature 1 (basic pokemon query)
@app.route('/pokedex', methods=['POST'])
def all_pokemon():
    data = request.get_json()
    print(data)

    pokemonConstraints = ['0 = 0'] # always true, used cuz i'm lazy and don't want to write queries with and without WHERE lol
    for key, val in data['pokemonInfo'].items():
        if len(val) == 0:
            continue
        if key.startswith('max'):
            pokemonConstraints.append(key[3:] + ' <= ' + val)
        elif key.startswith('min'):
            pokemonConstraints.append(key[3:] + ' >= ' + val)
        elif key == 'types':
            print(val)
            joined = '\',\''.join(val)
            pokemonConstraints.append('(type1 IN (\'' + joined + '\') OR type2 IN (\'' + joined + '\'))')
        else:
            try:
                int(val)
                pokemonConstraints.append(key + ' = ' + val)
            except:
                pokemonConstraints.append(key + ' ILIKE \'%' + val + '%\'')
    # # POKEMON INFO
    # name = data['pokemonInfo']['name']    # Name of pokemon user would like to filter for (empty means ALL)
    # types = data['pokemonInfo']['types']  # List of types user would like to filter for (empty means ALL)
    # # Note: the following have data type of String
    # # Empty string means user did not input anything, otherwise input is an integer (may be negative)
    # id = data['pokemonInfo']['id']
    # hp = data['pokemonInfo']['hp']
    # spd = data['pokemonInfo']['spd']
    # atk = data['pokemonInfo']['atk']
    # defense = data['pokemonInfo']['def']
    # spAtk = data['pokemonInfo']['spAtk']
    # spDef = data['pokemonInfo']['spDef']
    moveConstraints = []
    for key, val in data['moveInfo'].items():
        if len(val) == 0:
            continue
        if key.startswith('max'):
            moveConstraints.append(key[3:] + ' <= ' + val)
        elif key.startswith('min'):
            moveConstraints.append(key[3:] + ' >= ' + val)
        elif key == 'types':
            joined = '\',\''.join(val)
            moveConstraints.append('moveType IN (\'' + joined + '\')')
        elif key == 'name' or key == 'moveName':
            moveConstraints.append('Move.moveName' + ' ILIKE \'%' + val + '%\'')
        else:
            try:
                int(val)
                moveConstraints.append(key + ' = ' + val)
            except:
                moveConstraints.append(key + ' ILIKE \'%' + val + '%\'')

    # # MOVE INFO
    # moveName = data['moveInfo']['name']   # Name of learnable move user would like to filter for (empty means ALL)
    # moveTypes = data['moveInfo']['types']
    # # One of: Physical, Special
    # moveDmgType = data['moveInfo']['damageType']
    # # Note: the following have data type of String
    # # Empty string means user did not input anything, otherwise input is an integer (may be negative)
    # movePP = data['moveInfo']['pp']
    # movePower = data['moveInfo']['power']
    # moveAcc = data['moveInfo']['accuracy']

    if len(moveConstraints) == 0:
        cur.execute('''
            SELECT id, name, baseHp, baseSpd, baseAtk, baseDef, baseSpAtk, baseSpDef, type1, type2
            FROM Pokemon
            WHERE {0}
            ORDER BY id
            '''.format(
                ' AND '.join(pokemonConstraints)
            )
        )

        # print('test', sys.stderr)

        # for id, name, baseHp, baseSpd, baseAtk, baseDef, baseSpAtk, baseSpDef, type1, type2 in cur:
        #     print(name, file=sys.stderr)

        pokemon = [[
                {
                    'id': id,
                    'name': name,
                    'types': (type1, type2) if type2 else (type1,),
                    'colors': (get_color_by_type(type1),get_color_by_type(type2)) if type2 else (get_color_by_type(type1),),
                    'hp': baseHp,
                    'spd': baseSpd,
                    'atk': baseAtk,
                    'def': baseDef,
                    'spAtk': baseSpAtk,
                    'spDef': baseSpDef,
                }
                for id, name, baseHp, baseSpd, baseAtk, baseDef, baseSpAtk, baseSpDef, type1, type2 in cur
        ],]
        return jsonify({
            'status': 'success',
            'pokemon': pokemon
        })
    else:
        # TO-DO: Get from database and transform to proper format for front-end
        cur.execute('''
            SELECT id, name, baseHp, baseSpd, baseAtk, baseDef, baseSpAtk, baseSpDef, type1, type2, STRING_AGG(Move.moveName, ', ' ORDER BY Move.moveName) 
                FROM (
                (
                    Pokemon
                    JOIN
                    CanLearnMove
                    ON id=pid
                )
                JOIN 
                Move
                ON Move.moveName = CanLearnMove.moveName
            )
            WHERE
            ({0}) AND ({1})
            GROUP BY id, name, baseHp, baseSpd, baseAtk, baseDef, baseSpAtk, baseSpDef, type1, type2
            ORDER BY id
            '''.format(' AND '.join(pokemonConstraints), ' AND '.join(moveConstraints)))

        # print('test', sys.stderr)

        # for id, name, baseHp, baseSpd, baseAtk, baseDef, baseSpAtk, baseSpDef, type1, type2, moves in cur:
        #     print(name, file=sys.stderr)

        pokemon = [[
                {
                    'id': id,
                    'name': name,
                    'types': (type1, type2) if type2 else (type1,),
                    'colors': (get_color_by_type(type1),get_color_by_type(type2)) if type2 else (get_color_by_type(type1),),
                    'hp': baseHp,
                    'spd': baseSpd,
                    'atk': baseAtk,
                    'def': baseDef,
                    'spAtk': baseSpAtk,
                    'spDef': baseSpDef,
                    'moves': moves
                }
                for id, name, baseHp, baseSpd, baseAtk, baseDef, baseSpAtk, baseSpDef, type1, type2, moves in cur
        ],]
        return jsonify({
            'status': 'success',
            'pokemon': pokemon
        })

# This route is for feature 2 (recursive query)
@app.route('/evolutions', methods=['POST'])
def get_evolutions():
    data = request.get_json()

    # POKEMON INFO
    name = data['pokemonInfo']['name']    # Name of pokemon user would like to filter for (empty means ALL)
    types = data['pokemonInfo']['types']  # List of types user would like to filter for (empty means ALL)
    # Note: the following have data type of String
    # Empty string means user did not input anything, otherwise input is an integer (may be negative)
    id = data['pokemonInfo']['id']
    hp = data['pokemonInfo']['hp']
    spd = data['pokemonInfo']['spd']
    atk = data['pokemonInfo']['atk']
    defense = data['pokemonInfo']['def']
    spAtk = data['pokemonInfo']['spAtk']
    spDef = data['pokemonInfo']['spDef']

    # MOVE INFO
    moveName = data['moveInfo']['name']   # Name of learnable move user would like to filter for (empty means ALL)
    moveTypes = data['moveInfo']['types']
    # One of: Physical, Special
    moveDmgType = data['moveInfo']['damageType']
    # Note: the following have data type of String
    # Empty string means user did not input anything, otherwise input is an integer (may be negative)
    movePP = data['moveInfo']['pp']
    movePower = data['moveInfo']['power']
    moveAcc = data['moveInfo']['accuracy']

    # TO-DO: Get from database and transform to proper format for front-end

    return jsonify({
        'status': 'success',
        'pokemon': [POKEMON[0],],
    })

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route("/test")
def test():
    return jsonify("Success!")

if __name__ == "main":
    app.run()