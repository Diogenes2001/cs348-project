import pandas
import psycopg2
import ast
import os
from collections import defaultdict

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

def importTeams():
    directory = os.fsencode("../scraping")

    teamids = set()

    cur.execute("prepare pokemonExists2 as SELECT id FROM Pokemon WHERE name=$1")
    cur.execute("prepare getTeam as SELECT teamID, wins, losses FROM Team "
        "WHERE pid1 = $1 AND pid2 = $2 AND pid3 = $3 AND pid4 = $4 AND pid5 = $5 AND pid6 = $6 AND starter = $7")
    cur.execute("prepare createTeam as INSERT INTO Team VALUES (DEFAULT, $1, $2, $3, $4, $5, $6, $7, $8, $9)")
    cur.execute("prepare updateTeam as UPDATE Team SET wins = $1, losses = $2 WHERE teamID = $3")

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"): 
            try:
                data = pandas.read_csv("../scraping/" + filename, encoding='cp1252') # this allows for decoding of ' (single quote)
                for idx, info in data.iterrows():
                    if info['gameID'] + info['player'] not in teamids:
                        teamids.add(info['gameID']+info['player'])

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

                            cur.execute("execute pokemonExists2 ({0})".format("'" + name + "'"))
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
            except:
                print("Could not get team froms {0}, skipping".format(filename))


def importPokemonPairings():
    print("Importing Pokemon pairings...")

    # prepare an insert statement
    cur.execute(
        "prepare pokemonPairingsInsert as "
        "INSERT INTO PokemonPairings(pid1, pid2, Percentage) "
        "VALUES ($1, $2, $3)"
    )

    pokemon_name_to_id_map = {}
    pokemon = pandas.read_csv('PokemonDatabase.csv')
    for idx, info in pokemon.iterrows():
        pokemon_name_to_id_map[info['PokemonName']] = info['PokedexNumber']

    with open('moveset-gen8ou-1825.txt', 'r') as f:
        lines = f.readlines()

    num_lines = len(lines)

    breaks = list(filter(lambda line_num : lines[line_num] == lines[0], list(range(num_lines))))
    pokemon_starts = list(filter(lambda break_num : break_num == 0 or breaks[break_num] == breaks[break_num - 1] + 1,
                                 list(range(len(breaks)))))
    pokemon_pairings = defaultdict(int)
    for start in pokemon_starts:
        start_line_num = breaks[start]
        pname1 = " ".join(lines[start_line_num + 1].split()[1:-1])
        if pname1 in pokemon_name_to_id_map:
            pid1 = pokemon_name_to_id_map[pname1]

            line_num = start_line_num + 1
            teammates = False
            while True:
                if 'Teammates' in lines[line_num]:
                    teammates = True
                elif teammates:
                    if line_num in breaks:
                        break

                    parts = lines[line_num].split()[1:-1]
                    pname2 = " ".join(parts[:-1])
                    if pname2 in pokemon_name_to_id_map:
                        pid2 = pokemon_name_to_id_map[pname2]
                        percentage = float(parts[-1][:-1]) / 100

                        if pid1 < pid2:
                            pokemon_pairings[(pid1, pid2)] += percentage / 2
                        else:
                            pokemon_pairings[(pid2, pid1)] += percentage / 2

                line_num += 1

    for (pid1, pid2), percentage in pokemon_pairings.items():
        cur.execute("execute pokemonPairingsInsert({0}, {1}, {2})".format(pid1, pid2, percentage))
    conn.commit()

    print("Finished importing Pokemon pairings...")


#
# choose what to import down here
#

importTypes()
importPokemon()
importMoves()
importCanLearnMove()
importEffectiveness()
importTeams()
importPokemonPairings()

cur.close()
