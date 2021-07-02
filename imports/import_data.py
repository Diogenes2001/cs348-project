import pandas
import psycopg2
import ast
import os

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
            #print("Adding evolution to " + str(info['PokedexNumber']) + " " + str(info['Pre-EvolutionPokemonId']))
            other = pokemon.loc[pokemon['PokemonId'] == info['Pre-EvolutionPokemonId']].iloc[0]
            nr = other['PokedexNumber']
            #print(str(info['Pre-EvolutionPokemonId']) + " " + str(other['PokemonId']) + " " + str(nr))
            #print(other)
            cur.execute("execute updateEvolution ({0}, {1})".format(nr, info['PokedexNumber']))
    
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


def importTeams():
    directory = os.fsencode("../scraping")

    teamids = set()

    cur.execute("prepare pokemonExists as SELECT id FROM Pokemon WHERE name=$1")
    cur.execute("prepare getTeam as SELECT teamID, wins, losses FROM Team "
        "WHERE pid1 = $1 AND pid2 = $2 AND pid3 = $3 AND pid4 = $4 AND pid5 = $5 AND pid6 = $6 AND starter = $7")
    cur.execute("prepare createTeam as INSERT INTO Team VALUES (DEFAULT, $1, $2, $3, $4, $5, $6, $7, $8, $9)")
    cur.execute("prepare updateTeam as UPDATE Team SET wins = $1, losses = $2 WHERE teamID = $3")

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"): 
            data = pandas.read_csv("../scraping/" + filename)
            for idx, info in data.iterrows():
                if info['gameID'] not in teamids:
                    teamids.add(info['gameID'])

                    foundall = True
                    # try to find all pokemon in the database
                    pokemon = []
                    for i in range(1,7):
                        if pandas.isna(info['pokemon' + str(i)]):
                            foundall = False
                            break
                        name, *vals = info['pokemon' + str(i)].split(',')

                        if name.find('-') and name not in ['Ho-Oh', 'Porygon-Z', 'Jangmo-o', 'Hakamo-o', 'Kommo-o']:
                            name, *app = name.split('-')

                        cur.execute("execute pokemonExists ({0})".format("'" + name + "'"))
                        tup = cur.fetchone()

                        if tup is not None:
                            pokemon.append(tup[0])
                        else:
                            foundall = False
                            print("Could not find " + name)
                            break

                    if not foundall:
                        break

                    # if found all pokemon, retrieve id of that team

                    starter = pokemon[0]
                    pokemon.sort()
                    starter = pokemon.index(starter) + 1

                    cur.execute("execute getTeam ({0}, {1}, {2}, {3}, {4}, {5}, {6})".format(
                        pokemon[0], pokemon[1], pokemon[2], pokemon[3], pokemon[4], pokemon[5], starter
                    ))

                    tup = cur.fetchone()

                    if tup is not None:
                        id = tup[0]
                        wins = tup[1]
                        losses = tup[2]

                        if info['win']:
                            wins += 1
                        else:
                            losses += 1
                        
                        cur.execute("execute updateTeam ({0}, {1}, {2})".format(wins, losses, id))

                    else:
                        wins = 0
                        losses = 0
                        if info['win']:
                            wins = 1
                        else:
                            losses = 1

                        cur.execute("execute createTeam ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8})".format(
                            pokemon[0], pokemon[1], pokemon[2], pokemon[3], pokemon[4], pokemon[5], starter,
                            wins, losses
                        ))

                    # update database after each team was added
                    conn.commit()



#
# choose what to import down here
#

#importTypes()
importPokemon()
#importMoves()
#importCanLearnMove()
#importTeams()

cur.close()