import psycopg2
import random
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

conn = psycopg2.connect(host="localhost",
    database="Flask", user="postgres", password="password")
cur = conn.cursor()

def createQuery(pid, user):
    genders = ['male', 'female', 'unknown']
    query = '''INSERT INTO OwnedPokemon VALUES
              (DEFAULT, {}, '{}', DEFAULT,
              {}, '{}', '{}', {}, {}, {}, {}, {}, {}, '{}', '{}', NULL, NULL, NULL)'''

    # find possible moves for the pokemon
    try:
        cur.execute('''
            SELECT moveName FROM CanLearnMove WHERE pid={}
            '''.format(pid)
        )
        move = cur.fetchone()
        if move is None:
            return ""
        move = move[0]
    except:
        print("Failed to find moveName for pid " + str(pid))

    # find ability for the pokemon
    try:
        cur.execute('''
            SELECT ability1 FROM Pokemon WHERE id={}
            '''.format(pid)
        )
        ability = cur.fetchone()
        if ability is None:
            return ""
        ability = ability[0]
    except:
        print("Failed to find ability for pid " + str(pid))

    # generate random values for the fields
    level = random.randint(1, 100)
    gender = genders[random.randint(0, 2)]
    shiny = "false"
    makeShiny = random.randint(1, 8192)
    if makeShiny == 5555:
        shiny = "true"
    hp = random.randint(0, 100)
    atk = random.randint(0, 100)
    defense = random.randint(0, 100)
    spAtk = random.randint(0, 100)
    spDef = random.randint(0, 100)
    spd = random.randint(0, 100)

    return query.format(
        pid, user, level, gender, shiny, hp, atk, defense, spAtk, spDef, spd, ability, move
    )


def generateUserPokemon():
    # generate some users first
    try:
        pw_hash1 = bcrypt.generate_password_hash('pass1').decode('utf-8')
        cur.execute('''INSERT INTO "User" VALUES ('user1', 'user1@gmail.com','{0}')'''.format(pw_hash1))
        pw_hash2 = bcrypt.generate_password_hash('pass2').decode('utf-8')
        cur.execute('''INSERT INTO "User" VALUES ('user2', 'user2@gmail.com','{0}')'''.format(pw_hash2))
        pw_hash3 = bcrypt.generate_password_hash('pass3').decode('utf-8')
        cur.execute('''INSERT INTO "User" VALUES ('user3', 'user3@gmail.com','{0}')'''.format(pw_hash3))
        conn.commit()
        print("Successfully created users!")
    except:
        conn.rollback()

    # obtain all pokemon id's
    try:
        cur.execute('''SELECT id FROM Pokemon''')
        pokemonIds = [row[0] for row in cur.fetchall()]
        totalIds = len(pokemonIds)
    except:
        conn.rollback()
        print("Failed to find Pokemon")
        return

    # user 1, generate 50 pokemon
    for i in range(50):
        # select pokemon randomly
        pid = random.randrange(0, totalIds)
        query = createQuery(pid, 'user1')
        if query:
            try:
                cur.execute(query)
            except:
                print("Failed to execute: " + query)
                conn.rollback()

    print("Successfully created user 1's Pokemon!")
    conn.commit()

    # user 2, generate 10 pokemon
    for i in range(10):
        # select pokemon randomly
        pid = random.randrange(0, totalIds)
        query = createQuery(pid, 'user2')
        if query:
            try:
                cur.execute(query)
            except:
                print("Failed to execute: " + query)
                conn.rollback()

    print("Successfully created user 2's Pokemon!")
    conn.commit()

generateUserPokemon()
cur.close()