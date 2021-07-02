import pandas
import psycopg2
import ast

conn = psycopg2.connect(host="localhost",
    database="Flask", user="postgres", password="password")
cur = conn.cursor()

#
#  Types
#

def importTypes():
    cur.execute('''INSERT INTO "Type" VALUES ('Normal')''')
    cur.execute('''INSERT INTO "Type" VALUES ('Fire')''')
    cur.execute('''INSERT INTO "Type" VALUES ('Water')''')
    cur.execute('''INSERT INTO "Type" VALUES ('Grass')''')
    cur.execute('''INSERT INTO "Type" VALUES ('Electric')''')
    cur.execute('''INSERT INTO "Type" VALUES ('Ice')''')
    cur.execute('''INSERT INTO "Type" VALUES ('Fighting')''')
    cur.execute('''INSERT INTO "Type" VALUES ('Poison')''')
    cur.execute('''INSERT INTO "Type" VALUES ('Ground')''')
    cur.execute('''INSERT INTO "Type" VALUES ('Flying')''')
    cur.execute('''INSERT INTO "Type" VALUES ('Psychic')''')
    cur.execute('''INSERT INTO "Type" VALUES ('Bug')''')
    cur.execute('''INSERT INTO "Type" VALUES ('Rock')''')
    cur.execute('''INSERT INTO "Type" VALUES ('Ghost')''')
    cur.execute('''INSERT INTO "Type" VALUES ('Dark')''')
    cur.execute('''INSERT INTO "Type" VALUES ('Dragon')''')
    cur.execute('''INSERT INTO "Type" VALUES ('Steel')''')
    cur.execute('''INSERT INTO "Type" VALUES ('Fairy')''')

    conn.commit()

    print("Added types.")

#
#  Pokemon
#

def importPokemon():

    print('Going to import pokemon data...')

    pokemon = pandas.read_csv('PokemonDatabase.csv')

    # prepare an insert statement

    cur.execute(
        "prepare pokemonInsert as "
        "INSERT INTO Pokemon (id, name, baseHp, baseSpd, baseAtk, "
        "baseDef, baseSpAtk, baseSpDef, type1, type2, ability1, "
        "ability2, evolvesFromId, isLegendary, isMythical) " 
        "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10 ,"
        "$11, $12, $13, $14, $15)"
    )

    # process each line of the pokemon data and insert into database if applicable

    for idx, info in pokemon.iterrows():
        # check whether this should be inserted

        # need to have "alternate form name" = null
        if pandas.isna(info['AlternateFormName']):

            # extract values where not exactly equal to value in info

            type2 = info['SecondaryType']
            if (pandas.isna(type2)):
                type2 = "NULL"
            else:
                type2 = "'" + type2 + "'"
            
            ability2 = info['SecondaryAbility']
            if (pandas.isna(ability2)):
                ability2 = "NULL"
            else:
                ability2 = "'" + ability2 + "'"

            evolvesFromId = info['Pre-EvolutionPokemonId']
            if (pandas.isna(evolvesFromId)):
                evolvesFromId = "NULL"

            isLegendary = False
            isMythical = False
            if info['LegendaryType'] == "Legendary":
                isLegendary = True
            if info['LegendaryType'] == "Mythical":
                isMythical = True

            # insert values
            cur.execute('''execute pokemonInsert ({0}, {1}, {2}, {3}, {4}, {5}, {6}, 
                {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14})'''.format(
                    info['PokedexNumber'], "'" + info['PokemonName'] + "'", info['HealthStat'],
                    info['SpeedStat'], info['AttackStat'], info['DefenseStat'], 
                    info['SpecialAttackStat'], info['SpecialDefenseStat'],
                    "'" + info['PrimaryType'] + "'", type2, "'" + info['PrimaryAbility'] + "'", 
                    ability2, "NULL", isLegendary, isMythical
                )
            )

    conn.commit()

    # add evolvesFromId

    cur.execute("prepare updateEvolution as UPDATE Pokemon SET evolvesFromId = $1 WHERE id = $2")

    for idx, info in pokemon.iterrows():
        # check whether this should be inserted
        
        # need to have "alternate form name" = null
        if pandas.isna(info['AlternateFormName']) and not pandas.isna(info['Pre-EvolutionPokemonId']):
            cur.execute("execute updateEvolution ({0}, {1})".format(info['PokedexNumber'], info['Pre-EvolutionPokemonId']))
    
    conn.commit()

    print('Import of Pokemon data finished.')

#
# Move
#

def importMoves():

    moves = pandas.read_csv('move-data.csv')

    cur.execute('''prepare moveInsert as INSERT INTO Move VALUES 
        ($1, $2, $3, $4, $5, $6)''')

    for idx, info in moves.iterrows():
        # check whether this should be inserted
        # need to have move category not status

        power = info['Power']
        if power == "None":
            power = "NULL"

        accuracy = info['Accuracy']
        if accuracy == "None":
            accuracy = "NULL"

        if not info['Category'] == "Status":
            cur.execute("execute moveInsert ({0}, {1}, {2}, {3}, {4}, {5})".format(
                "'" + info['Name'] + "'", "'" + info['Type'] + "'", info['PP'],
                power, "'" + info['Category'].lower() + "'", accuracy
            ))
    
    conn.commit()

#
# CanLearnMove
#

def importCanLearnMove():
    canLearnMove = pandas.read_csv("pokemon-data.csv", sep=';')
    
    cur.execute("prepare pokemonExists as SELECT id FROM Pokemon WHERE name=$1")
    cur.execute("prepare moveExists as SELECT moveName FROM Move WHERE moveName=$1")
    cur.execute("prepare canLearnInsert as INSERT INTO CanLearnMove VALUES ($1,$2)")

    for idx, info in canLearnMove.iterrows():

        # query database to see if this pokemon is one we keep track of and get its id
        cur.execute("execute pokemonExists ({0})".format("'" + info['Name'] + "'"))
        tup = cur.fetchone()

        if tup is not None:

            id = tup[0]
            # parse moves column
            moves = ast.literal_eval(info['Moves'])
            moves = list(dict.fromkeys(moves))

            for move in moves:
                cur.execute("execute moveExists ({0})".format("'" + move + "'"))
                if cur.fetchone() is not None:
                    # add to DB instead of printing :)
                    cur.execute("execute canLearnInsert ({0}, {1})".format(id, "'" + move + "'"))
    
    conn.commit()

def importEffectiveness():
    print("Importing type effectiveness...")
    types = ['Normal', 'Fire', 'Water', 'Grass', 'Electric', 'Ice', 'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dark', 'Dragon', 'Steel', 'Fairy']
    effectiveness = pandas.read_csv('effectiveness.csv')

    cur.execute('''prepare effectivenessInsert as INSERT INTO Effectiveness VALUES 
        ($1, $2, $3)''')

    d = dict()
    for t in types:
        d[t] = dict()
    for idx, info in effectiveness.iterrows():
        d[info['moveType']][info['pokemonType']] = info['effectiveness']
    for t1 in types:
        for t2 in types:
            if t2 not in d[t1]:
                d[t1][t2] = '1'
            cur.execute("execute effectivenessInsert ({0}, {1}, {2})".format(
                "'" + t1 + "'", "'" + t2 + "'", d[t1][t2]
            ))
    
    conn.commit()
    print("Finished importing type effectiveness")

#
# choose what to import down here
#

# importTypes()
# importPokemon()
# importMoves()
# importCanLearnMove()
# importEffectiveness()

cur.close()