import json
from flask import Flask, request, json, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import psycopg2
import sys
import threading

app = Flask(__name__)
bcrypt = Bcrypt(app)

# connect to the database
conn = psycopg2.connect(host="localhost",
    database="Flask", user="postgres", password="password")
cur = conn.cursor()

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

dbLock = threading.Lock()

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

    dbLock.acquire()
    cur.execute('''SELECT password FROM "User" WHERE username=%s''',[data['username']])

    tup = cur.fetchone()
    dbLock.release()
    if tup is not None:
        passw = tup[0]

        if bcrypt.check_password_hash(passw, data['password']):

            dbLock.acquire()
            cur.execute('''DELETE FROM "User" WHERE username=%s ''', [data['username']])

            conn.commit()
            dbLock.release()

            return jsonify({'status': 'success', 'error': 'Successfully deleted your account.'})

    return jsonify({'status': 'failure', 'error': 'The password was incorrect.'})

@app.route('/changepass', methods=['POST'])
def try_changepass():
    data = request.get_json()

    dbLock.acquire()
    cur.execute('''SELECT password FROM "User" WHERE username=%s ''', [data['username']])

    tup = cur.fetchone()
    dbLock.release()
    if tup is not None:
        passw = tup[0]

        if bcrypt.check_password_hash(passw, data['curpass']):

            pw_hash = bcrypt.generate_password_hash(data['newpass']).decode('utf-8')
            dbLock.acquire()
            cur.execute('''UPDATE "User" SET password = %s WHERE username= %s ''', [pw_hash, data['username']])

            conn.commit()
            dbLock.release()

            return jsonify({'status': 'success', 'error': 'Successfully updated your password.'})

    return jsonify({'status': 'failure', 'error': 'Current password was incorrect.'})

@app.route('/signup', methods=['POST'])
def try_signup():
    data = request.get_json()

    dbLock.acquire()
    cur.execute('''SELECT * FROM "User" WHERE username= %s ''', [data['username']])

    tup = cur.fetchone()
    dbLock.release()
    if tup is not None:
        return jsonify({ 'status': 'failure', 'error': 'Username is already taken.'})

    pw_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    dbLock.acquire()
    cur.execute('''INSERT INTO "User" VALUES (%s, %s, %s) ''', [data['username'], data['email'], pw_hash])

    conn.commit()
    dbLock.release()

    return jsonify({
        'status': 'success'
    })

@app.route('/login', methods=['POST'])
def try_login():
    data = request.get_json()

    dbLock.acquire()
    cur.execute('''SELECT password FROM "User" WHERE username= %s ''', [data['username']])

    tup = cur.fetchone()
    dbLock.release()
    if tup is not None:
        passw = tup[0]

        if bcrypt.check_password_hash(passw, data['password']):
            return jsonify({
                'status': 'success'
            })

    return jsonify({ 'status': 'failure', 'error': 'Username or password is incorrect.'})

# This route is for feature 1 (basic pokemon query)
@app.route('/pokedex', methods=['POST'])
def all_pokemon():
    data = request.get_json()
    print(data)

    user_values = []

    pokemonConstraints = ['0 = 0'] # always true, used cuz i'm lazy and don't want to write queries with and without WHERE lol
    for key, val in data['pokemonInfo'].items():
        if len(val) == 0:
            continue
        if key.startswith('max'):
            pokemonConstraints.append(key[3:] + ' <= %s')
            user_values.append(val)
        elif key.startswith('min'):
            pokemonConstraints.append(key[3:] + ' >= %s')
            user_values.append(val)
        elif key == 'types':
            placeholders = ['%s' for i in val]
            print(val)
            user_values = user_values + val + val
            joined = ','.join(placeholders)
            pokemonConstraints.append('(type1 IN (' + joined + ') OR type2 IN (' + joined + '))')
        else:
            try:
                int(val)
                pokemonConstraints.append(key + ' = %s')
                user_values.append(val)
            except:
                pokemonConstraints.append(key + ' ILIKE %s')
                user_values.append('%' + val + '%')
    if len(data['effectiveness']['weaknesses']) > 0 or len(data['effectiveness']['resistances']) > 0:
        valid_types = None
        for type in data['effectiveness']['weaknesses']:
            dbLock.acquire()
            cur.execute('''
                (
                    SELECT e1.pokemonType, e2.pokemonType FROM Effectiveness AS e1, Effectiveness AS e2 
                    WHERE e1.moveType = %s AND e2.moveType = %s AND (e1.effectiveness * e2.effectiveness) > 1
                    AND e1.pokemonType > e2.pokemonType
                ) UNION (
                    SELECT pokemonType, NULL FROM Effectiveness WHERE moveType = %s AND effectiveness > 1
                )
            ''', [type, type, type])
            dbLock.release()
            
            types = set((c1, c2) for c1, c2 in cur)
            if valid_types is None:
                valid_types = types
            else:
                valid_types = valid_types.intersection(types)
                if len(valid_types) == 0:
                    return jsonify({
                        'status': 'success',
                        'pokemon': []
                    })
        for type in data['effectiveness']['resistances']:
            dbLock.acquire()
            cur.execute('''
                (
                    SELECT e1.pokemonType, e2.pokemonType FROM Effectiveness AS e1, Effectiveness AS e2 
                    WHERE e1.moveType = %s AND e2.moveType = %s AND (e1.effectiveness * e2.effectiveness) < 1
                    AND e1.pokemonType > e2.pokemonType
                ) UNION (
                    SELECT pokemonType, NULL FROM Effectiveness WHERE moveType = %s AND effectiveness < 1
                )
            ''', [type, type, type])
            dbLock.release()
            
            types = set((c1, c2) for c1, c2 in cur)
            if valid_types is None:
                valid_types = types
            else:
                valid_types = valid_types.intersection(types)
                if len(valid_types) == 0:
                    return jsonify({
                        'status': 'success',
                        'pokemon': []
                    })
        type_contraint = ' OR '.join([
                '(type1 = \'{0}\' AND type2 = \'{1}\') OR (type1 = \'{1}\' AND type2 = \'{0}\')'.format(v[0], v[1])
                if v[1] is not None
                else '(type1 = \'{0}\' AND type2 IS NULL)'.format(v[0])
             for v in valid_types
             ])
        pokemonConstraints.append(type_contraint)

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
            moveConstraints.append(key[3:] + ' <= %s')
            user_values.append(val)
        elif key.startswith('min'):
            moveConstraints.append(key[3:] + ' >= %s')
            user_values.append(val)
        elif key == 'types':
            placeholders = ['%s' for i in val]
            user_values = user_values + val
            joined = ','.join(placeholders)
            moveConstraints.append('moveType IN (' + joined + ')')
        elif key == 'name' or key == 'moveName':
            moveConstraints.append('Move.moveName' + ' ILIKE %s')
            user_values.append('%' + val + '%')
        else:
            try:
                int(val)
                moveConstraints.append(key + ' = %s')
                user_values.append(val)
            except:
                moveConstraints.append(key + ' ILIKE %s')
                user_values.append('%' + val + '%')

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
        dbLock.acquire()
        cur.execute('''
            SELECT id, name, baseHp, baseSpd, baseAtk, baseDef, baseSpAtk, baseSpDef, type1, type2
            FROM Pokemon
            WHERE {0}
            ORDER BY id
            '''.format(
                ' AND '.join(pokemonConstraints)
            ), user_values
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
        dbLock.release()
        return jsonify({
            'status': 'success',
            'pokemon': pokemon
        })
    else:
        # TO-DO: Get from database and transform to proper format for front-end
        dbLock.acquire()
        cur.execute('''
            SELECT id, name, baseHp, baseSpd, baseAtk, baseDef, baseSpAtk, baseSpDef, type1, type2, STRING_AGG(Move.moveName, ', ' ORDER BY Move.moveName) 
                FROM (
                (
                    Pokemon
                    LEFT JOIN
                    CanLearnMove
                    ON id=pid
                )
                LEFT JOIN 
                Move
                ON Move.moveName = CanLearnMove.moveName
            )
            WHERE
            ({0}) AND ({1})
            GROUP BY id, name, baseHp, baseSpd, baseAtk, baseDef, baseSpAtk, baseSpDef, type1, type2
            ORDER BY id
            '''.format(' AND '.join(pokemonConstraints), ' AND '.join(moveConstraints)), user_values)

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
        dbLock.release()
        return jsonify({
            'status': 'success',
            'pokemon': pokemon
        })

@app.route('/pokemon', methods=['POST'])
def get_pokemon():
    data = request.get_json()
    id = data['id']
    dbLock.acquire()
    cur.execute('''
            SELECT id, name, baseHp, baseSpd, baseAtk, baseDef, baseSpAtk, baseSpDef, type1, type2, STRING_AGG(Move.moveName, ', ' ORDER BY Move.moveName) 
                FROM (
                (
                    Pokemon
                    LEFT JOIN
                    CanLearnMove
                    ON id=pid
                )
                LEFT JOIN 
                Move
                ON Move.moveName = CanLearnMove.moveName
            )
            WHERE
            (id=%s)
            GROUP BY id, name, baseHp, baseSpd, baseAtk, baseDef, baseSpAtk, baseSpDef, type1, type2
            ORDER BY id
            ''', [id]
            )
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
    cur.execute('''
            WITH RECURSIVE
            Evolution(evolvesFrom, evolvesInto) AS (
                (
                    SELECT evolvesFromId, id FROM Pokemon
                )
                UNION
                (
                    SELECT e1.evolvesFrom, id
                    FROM Evolution e1, Pokemon p
                    WHERE e1.evolvesInto = p.evolvesFromId
                )
            )
            SELECT id, name, baseHp, baseSpd, baseAtk, baseDef, baseSpAtk, baseSpDef, type1, type2, evolvesFromId FROM Pokemon
            WHERE id IN (
                SELECT evolvesInto
                FROM Evolution
                WHERE evolvesFrom = %s
            )
            ''', [id]
            )
    evolutions = [[
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
                    'evolvesFromId': evolvesFromId
                }
                for id, name, baseHp, baseSpd, baseAtk, baseDef, baseSpAtk, baseSpDef, type1, type2, evolvesFromId in cur
        ],]
    dbLock.release()
    idToName = dict()
    print(pokemon)
    print(id)
    idToName[int(id)] = pokemon[0][0]['name']
    for d in evolutions[0]:
        idToName[d['id']] = d['name']
    for d in evolutions[0]:
        d['evolvesFromName'] = idToName[d['evolvesFromId']]
    
    effectiveness = None
    types = pokemon[0][0]['types']
    dbLock.acquire()
    if len(types) == 2:
        cur.execute('''
            SELECT e1.moveType, (e1.effectiveness * e2.effectiveness)  FROM Effectiveness AS e1, Effectiveness AS e2 
            WHERE e1.pokemonType = %s AND e2.pokemonType = %s AND e1.moveType = e2.moveType
        ''', [types[0], types[1]])
    else:
        cur.execute('''
            SELECT moveType, effectiveness FROM Effectiveness WHERE pokemonType = %s
        ''', [types[0]])
    effectiveness = [
                {
                    'moveType': c1,
                    'color': get_color_by_type(c1),
                    'effectiveness': str(c2),
                }
                for c1, c2 in cur
    ]
    dbLock.release()
    
    return jsonify({
        'status': 'success',
        'pokemon': pokemon,
        'evolutions': evolutions,
        'effectiveness': effectiveness
    })

@app.route('/ownedpokemon', methods=['POST'])
def get_ownedpokemon():
    data = request.get_json()
    info = data['info']

    user_values = []
    conditions = ""

    if info['nickname']:
        conditions += " AND nickname ILIKE %s"
        user_values.append('%' + info['nickname'] + '%')
    if info['move']:
        conditions += " AND (move1 ILIKE %s OR move2 ILIKE %s OR move3 ILIKE %s OR move4 ILIKE %s)"
        user_values.append('%' + info['move'] + '%')
        user_values.append('%' + info['move'] + '%')
        user_values.append('%' + info['move'] + '%')
        user_values.append('%' + info['move'] + '%')
    if info['ability']:
        conditions += " AND ability ILIKE %s"
        user_values.append('%' + info['ability'] + '%')
    if info['gender']:
        conditions += " AND gender = %s"
        user_values.append(info['gender'])
    if info['shiny']:
        conditions += " AND isShiny = %s"
        user_values.append(info['shiny']) 

    user_values.append(data['username'])

    cur.execute('''
            SELECT ownedId, species, name, nickname, level, gender, isShiny, hp, atk, def, spAtk, spDef, spd, ability, move1, move2, move3, move4, type1, type2 
            FROM OwnedPokemon, Pokemon
            WHERE
            Pokemon.id = OwnedPokemon.species {0}
            AND
            owner = %s
            ORDER BY nickname
            '''.format(conditions), user_values)

    ownedpokemon = [[
                {
                    'ownedId': ownedId,
                    'species': species,
                    'speciesName': name,
                    'name': nickname,
                    'types': (type1, type2) if type2 else (type1,),
                    'colors': (get_color_by_type(type1),get_color_by_type(type2)) if type2 else (get_color_by_type(type1),),
                    'level': level,
                    'gender': gender,
                    'isShiny': isShiny,
                    'hp': hp,
                    'spd': spd,
                    'atk': atk,
                    'def': defence,
                    'spAtk': spAtk,
                    'spDef': spDef,
                    'ability': ability,
                    'move1': move1,
                    'move2': move2,
                    'move3': move3,
                    'move4': move4
                }
                for ownedId, species, name, nickname, level, gender, isShiny, hp, atk, defence, spAtk, spDef, spd, ability, move1, move2, move3, move4, type1, type2 in cur
        ],]

    return jsonify({
        'status': 'success',
        'ownedpokemon': ownedpokemon
    })

@app.route('/getspeciesinfo', methods=['POST'])
def getspeciesinfo():

    data = request.get_json()

    cur.execute('''
            SELECT id, baseHp, baseSpd, baseAtk, baseDef, baseSpAtk, baseSpDef, ability1, ability2
            FROM Pokemon
            WHERE name=%s
            ''', [data['species']]
        )

    info = [
                {
                    'id': id,
                    'hp': hp,
                    'spd': spd,
                    'atk': atk,
                    'def': defence,
                    'spAtk': spAtk,
                    'spDef': spDef,
                    'ability1': ability1,
                    'ability2': ability2
                }
                for id, hp, atk, defence, spAtk, spDef, spd, ability1, ability2 in cur
        ]

    return jsonify({
        'status': 'success',
        'pokemon': info
    })

@app.route('/createownedpokemon', methods=['POST'])
def createownedpokemon():

    data = request.get_json()
    info = data['createInfo']

    error = ''
    status = 'success'

    shiny = False
    if (info['shiny'] == 'TRUE'):
        shiny = True

    columns = "(species, owner, isShiny, gender, ability, move1"
    values = "(%s, %s, %s, %s, %s, %s"
    user_values = [info['id'], data['username'], shiny, info['gender'], info['ability'], info['move1']]

    if info['nickname']:
        columns += ", nickname"
        values += ", %s"
        user_values.append(info['nickname'])
    if info['level']:
        columns += ", level"
        values += ", %s"
        user_values.append(info['level'])
    if info['hp']:
        columns += ", hp"
        values += ", %s"
        user_values.append(info['hp'])
    if info['atk']:
        columns += ", atk"
        values += ", %s"
        user_values.append(info['atk'])
    if info['def']:
        columns += ", def"
        values += ", %s"
        user_values.append(info['def'])
    if info['spAtk']:
        columns += ", spAtk"
        values += ", %s"
        user_values.append(info['spAtk'])
    if info['spDef']:
        columns += ", spDef"
        values += ", %s"
        user_values.append(info['spDef'])
    if info['spd']:
        columns += ", spd"
        values += ", %s"
        user_values.append(info['spd'])
    if info['move2']:
        columns += ", move2"
        values += ", %s"
        user_values.append(info['move2'])
    if info['move3']:
        columns += ", move3"
        values += ", %s"
        user_values.append(info['move3'])
    if info['move4']:
        columns += ", move4"
        values += ", %s"
        user_values.append(info['move4'])

    columns += ")"
    values += ")"

    try:
        cur.execute('''
                INSERT INTO OwnedPokemon {0}
                VALUES {1};
                '''.format(columns, values), user_values
            )
    except Exception as err:
        error = str(err)
        status = 'failure'

    conn.commit()

    return jsonify({
        'status': status,
        'error': error
    })

@app.route('/changeownedpokemon', methods=['POST'])
def changeownedpokemon():

    data = request.get_json()

    error = ''
    status = 'success'

    try:
        cur.execute('''
                UPDATE OwnedPokemon 
                SET nickname = %s, level = %s, hp = %s, spd = %s, atk = %s, def = %s, spAtk = %s,
                    spDef = %s, move1 = %s, move2 = %s, move3 = %s, move4 = %s
                WHERE ownedId = %s;
                ''', [data['nickname'], data['level'], data['hp'], data['spd'], data['atk'], 
                data['def'], data['spAtk'], data['spDef'], data['move1'], data['move2'] if data['move2'] else None, 
                data['move3'] if data['move3'] else None, data['move4'] if data['move3'] else None, data['ownedId']]
            )
    except Exception as err:
        error = str(err)
        status = 'failure'

    conn.commit()

    return jsonify({
        'status': status,
        'error': error
    })

@app.route('/deleteownedpokemon', methods=['POST'])
def deleteownedpokemon():

    data = request.get_json()

    cur.execute('''DELETE FROM OwnedPokemon WHERE ownedId = %s''', [data['ownedId']])

    conn.commit()

    return jsonify({
        'status': 'success'
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

@app.route('/program_generated_teams', methods=['POST'])
def program_generated_teams():
    data = request.get_json()
    pokemonNameFilter = data['pokemonNameFilter']

    user_values = []

    nameCond = ""
    if pokemonNameFilter:
        nameCond = "WHERE LOWER(Pokemon1.name) = LOWER(%s)"
        user_values.append(pokemonNameFilter)
    idCond = "" if pokemonNameFilter else "AND Pokemon1.id < Pokemon2.id"

    dbLock.acquire()
    cur.execute(f'''
        SELECT
            p1id,
            p1name,
            p2id,
            p2name,
            p3id,
            p3name,
            p4id,
            p4name,
            p5id,
            p5name,
            Pokemon6.id as p6id,
            Pokemon6.name as p6name
        FROM
            (SELECT
                p1id,
                p1name,
                p1type,
                p2id,
                p2name,
                p2type,
                p3id,
                p3name,
                p3type,
                p4id,
                p4name,
                p4type,
                Pokemon5.id as p5id,
                Pokemon5.name as p5name,
                Pokemon5.type1 as p5type
            FROM
                (SELECT
                    p1id,
                    p1name,
                    p1type,
                    p2id,
                    p2name,
                    p2type,
                    p3id,
                    p3name,
                    p3type,
                    Pokemon4.id as p4id,
                    Pokemon4.name as p4name,
                    Pokemon4.type1 as p4type
                FROM
                    (SELECT
                        p1id,
                        p1name,
                        p1type,
                        p2id,
                        p2name,
                        p2type,
                        Pokemon3.id as p3id,
                        Pokemon3.name as p3name,
                        Pokemon3.type1 as p3type
                    FROM
                        (SELECT
                            Pokemon1.id as p1id,
                            Pokemon1.name as p1name,
                            Pokemon1.type1 as p1type,
                            Pokemon2.id as p2id,
                            Pokemon2.name as p2name,
                            Pokemon2.type1 as p2type
                        FROM Pokemon as Pokemon1
                        INNER JOIN Pokemon as Pokemon2
                            ON Pokemon1.id <> Pokemon2.id
                            {idCond}
                            AND Pokemon1.type1 <> Pokemon2.type1
                        LEFT JOIN PokemonPairings as Pokemon12
                            ON 	Pokemon12.pid1 = Pokemon1.id
                            AND	Pokemon12.pid2 = Pokemon2.id
                        {nameCond}
                        ORDER BY
                            COALESCE(Pokemon12.percentage, 0) DESC
                        LIMIT 1000) as Pokemon12
                    INNER JOIN Pokemon as Pokemon3
                        ON  p1id <> Pokemon3.id
                        AND	p2id < Pokemon3.id
                        AND p1type <> Pokemon3.type1
                        AND p2type <> Pokemon3.type1
                    LEFT JOIN PokemonPairings as Pokemon13
                        ON 	Pokemon13.pid1 = p1id
                        AND	Pokemon13.pid2 = Pokemon3.id
                    LEFT JOIN PokemonPairings as Pokemon23
                        ON 	Pokemon23.pid1 = p2id
                        AND Pokemon23.pid2 = Pokemon3.id
                    ORDER BY
                        COALESCE(Pokemon13.percentage, 0) +
                        COALESCE(Pokemon23.percentage, 0) DESC
                    LIMIT 1000) as Pokemon123
                INNER JOIN Pokemon as Pokemon4
                    ON  p1id <> Pokemon4.id
                    AND p3id < Pokemon4.id
                    AND p1type <> Pokemon4.type1
                    AND p2type <> Pokemon4.type1
                    AND p3type <> Pokemon4.type1
                LEFT JOIN PokemonPairings as Pokemon14
                    ON 	Pokemon14.pid1 = p1id
                    AND	Pokemon14.pid2 = Pokemon4.id
                LEFT JOIN PokemonPairings as Pokemon24
                    ON 	Pokemon24.pid1 = p2id
                    AND	Pokemon24.pid2 = Pokemon4.id
                LEFT JOIN PokemonPairings as Pokemon34
                    ON 	Pokemon34.pid1 = p3id
                    AND	Pokemon34.pid2 = Pokemon4.id
                ORDER BY
                    COALESCE(Pokemon14.percentage, 0) +
                    COALESCE(Pokemon24.percentage, 0) +
                    COALESCE(Pokemon34.percentage, 0) DESC
                LIMIT 1000) as Pokemon1234
            INNER JOIN Pokemon as Pokemon5
                ON  p1id <> Pokemon5.id
                AND p4id < Pokemon5.id
                AND p1type <> Pokemon5.type1
                AND p2type <> Pokemon5.type1
                AND p3type <> Pokemon5.type1
                AND p4type <> Pokemon5.type1
            LEFT JOIN PokemonPairings as Pokemon15
                ON 	Pokemon15.pid1 = p1id
                AND	Pokemon15.pid2 = Pokemon5.id
            LEFT JOIN PokemonPairings as Pokemon25
                ON 	Pokemon25.pid1 = p2id
                AND	Pokemon25.pid2 = Pokemon5.id
            LEFT JOIN PokemonPairings as Pokemon35
                ON 	Pokemon35.pid1 = p3id
                AND	Pokemon35.pid2 = Pokemon5.id
            LEFT JOIN PokemonPairings as Pokemon45
                ON 	Pokemon45.pid1 = p4id
                AND	Pokemon45.pid2 = Pokemon5.id
            ORDER BY
                COALESCE(Pokemon15.percentage, 0) +
                COALESCE(Pokemon25.percentage, 0) +
                COALESCE(Pokemon35.percentage, 0) +
                COALESCE(Pokemon45.percentage, 0) DESC
            LIMIT 1000) as Pokemon12345
        INNER JOIN Pokemon as Pokemon6
            ON  p1id <> Pokemon6.id
            AND p5id < Pokemon6.id
            AND p1type <> Pokemon6.type1
            AND p2type <> Pokemon6.type1
            AND p3type <> Pokemon6.type1
            AND p4type <> Pokemon6.type1
            AND p5type <> Pokemon6.type1
        LEFT JOIN PokemonPairings as Pokemon16
            ON 	Pokemon16.pid1 = p1id
            AND	Pokemon16.pid2 = Pokemon6.id
        LEFT JOIN PokemonPairings as Pokemon26
            ON 	Pokemon26.pid1 = p2id
            AND	Pokemon26.pid2 = Pokemon6.id
        LEFT JOIN PokemonPairings as Pokemon36
            ON 	Pokemon36.pid1 = p3id
            AND	Pokemon36.pid2 = Pokemon6.id
        LEFT JOIN PokemonPairings as Pokemon46
            ON 	Pokemon46.pid1 = p4id
            AND	Pokemon46.pid2 = Pokemon6.id
        LEFT JOIN PokemonPairings as Pokemon56
            ON 	Pokemon56.pid1 = p5id
            AND	Pokemon56.pid2 = Pokemon6.id
        ORDER BY
            COALESCE(Pokemon16.percentage, 0) +
            COALESCE(Pokemon26.percentage, 0) +
            COALESCE(Pokemon36.percentage, 0) +
            COALESCE(Pokemon46.percentage, 0) +
            COALESCE(Pokemon56.percentage, 0) DESC
        LIMIT 5''', user_values)
    tups = cur.fetchall()
    dbLock.release()

    return jsonify({
        'status': 'success',
        'teams': [[[tup[0], tup[1]],
                   [tup[2], tup[3]],
                   [tup[4], tup[5]],
                   [tup[6], tup[7]],
                   [tup[8], tup[9]],
                   [tup[10], tup[11]]] for tup in tups]
    })

@app.route('/user_generated_teams', methods=['POST'])
def user_generated_teams():
    data = request.get_json()
    pokemonNameFilter = data['pokemonNameFilter']
    user_values = []
    if pokemonNameFilter:
        user_values = [pokemonNameFilter for i in range(6)]
    nameCond = lambda isWhere, field, last: (("AND (" if isWhere else "OR") + f" LOWER({field}) = LOWER(%s)" + (")" if last else "")) if pokemonNameFilter else ""

    dbLock.acquire()
    cur.execute(f'''
        SELECT pid1,
               Pokemon1.name,
               pid2,
               Pokemon2.name,
               pid3,
               Pokemon3.name,
               pid4,
               Pokemon4.name,
               pid5,
               Pokemon5.name,
               pid6,
               Pokemon6.name
        FROM Team
        INNER JOIN Pokemon as Pokemon1
        ON pid1 = Pokemon1.id
        INNER JOIN Pokemon as Pokemon2
        ON pid2 = Pokemon2.id
        INNER JOIN Pokemon as Pokemon3
        ON pid3 = Pokemon3.id
        INNER JOIN Pokemon as Pokemon4
        ON pid4 = Pokemon4.id
        INNER JOIN Pokemon as Pokemon5
        ON pid5 = Pokemon5.id
        INNER JOIN Pokemon as Pokemon6
        ON pid6 = Pokemon6.id
        WHERE wins + losses >= 2
        {nameCond(True, 'Pokemon1.name', False)}
        {nameCond(False, 'Pokemon2.name', False)}
        {nameCond(False, 'Pokemon3.name', False)}
        {nameCond(False, 'Pokemon4.name', False)}
        {nameCond(False, 'Pokemon5.name', False)}
        {nameCond(False, 'Pokemon6.name', True)}
        ORDER BY CAST(wins AS FLOAT) / CAST(wins + losses AS FLOAT) DESC
        LIMIT 5''', user_values)
    tups = cur.fetchall()
    dbLock.release()

    for i in range(len(tups)):
        if pokemonNameFilter:
            tups[i] = list(tups[i])
            if tups[i][3] == pokemonNameFilter:
                tups[i][0], tups[i][2] = tups[i][2], tups[i][0]
                tups[i][1], tups[i][3] = tups[i][3], tups[i][1]
            elif tups[i][5] == pokemonNameFilter:
                tups[i][0], tups[i][4] = tups[i][4], tups[i][0]
                tups[i][1], tups[i][5] = tups[i][5], tups[i][1]
            elif tups[i][7] == pokemonNameFilter:
                tups[i][0], tups[i][6] = tups[i][6], tups[i][0]
                tups[i][1], tups[i][7] = tups[i][7], tups[i][1]
            elif tups[i][9] == pokemonNameFilter:
                tups[i][0], tups[i][8] = tups[i][8], tups[i][0]
                tups[i][1], tups[i][9] = tups[i][9], tups[i][1]
            elif tups[i][11] == pokemonNameFilter:
                tups[i][0], tups[i][10] = tups[i][10], tups[i][0]
                tups[i][1], tups[i][11] = tups[i][11], tups[i][1]

    return jsonify({
        'status': 'success',
        'teams': [[[tup[0], tup[1]],
                   [tup[2], tup[3]],
                   [tup[4], tup[5]],
                   [tup[6], tup[7]],
                   [tup[8], tup[9]],
                   [tup[10], tup[11]]] for tup in tups]
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
