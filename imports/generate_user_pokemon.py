import psycopg2
import random

conn = psycopg2.connect(host="localhost",
    database="Flask", user="postgres", password="password")
cur = conn.cursor()

def createQuery(pid, user):
    genders = ['male', 'female', 'unknown']
    query = '''INSERT INTO OwnedPokemon VALUES
              (DEFAULT, {}, '{}', DEFAULT,
              {}, '{}', '{}', {}, {}, {}, {}, {}, {}, '{}', '{}', NULL, NULL, NULL)'''

    # find possible moves for the pokemon
    cur.execute('''
        SELECT moveName FROM CanLearnMove WHERE pid={}
        '''.format(pid)
    )
    move = cur.fetchone()
    if move is None:
        return ""
    move = move[0]

    # find ability for the pokemon
    cur.execute('''
        SELECT ability1 FROM Pokemon WHERE id={}
        '''.format(pid)
    )
    ability = cur.fetchone()
    if ability is None:
        return ""
    ability = ability[0]

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
        cur.execute('''INSERT INTO "User" VALUES ('user1', 'user1@gmail.com','pass1')''')
        cur.execute('''INSERT INTO "User" VALUES ('user2', 'user2@gmail.com','pass2')''')
        cur.execute('''INSERT INTO "User" VALUES ('user3', 'user3@gmail.com','pass3')''')
        conn.commit()
    except:
        conn.rollback()

    # obtain all pokemon id's
    try:
        cur.execute('''SELECT id FROM Pokemon''')
        pokemonIds = [row[0] for row in cur.fetchall()]
        totalIds = len(pokemonIds)
    except:
        conn.rollback()
        print("Failed")
        return

    # user 1, generate 50 pokemon
    for i in range(50):
        # select pokemon randomly
        pid = random.randrange(0, totalIds)
        query = createQuery(pid, 'user1')
        if query:
            cur.execute(query)

    conn.commit()

    # user 2, generate 10 pokemon
    for i in range(10):
        # select pokemon randomly
        pid = random.randrange(0, totalIds)
        query = createQuery(pid, 'user2')
        if query:
            cur.execute(query)

    conn.commit()

generateUserPokemon()
cur.close()