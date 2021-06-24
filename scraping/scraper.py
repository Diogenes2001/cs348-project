import requests
from bs4 import BeautifulSoup
import json
import csv
import datetime
import string
import time

while True:
    URL = 'https://replay.pokemonshowdown.com'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    links = soup.find_all('a')
    now = datetime.datetime.now()
    now_str = now.strftime("%Y-%m-%d-%H-%M")
    print("Running at " + now_str)
    with open('battles-' + now_str + '.csv', 'w', newline='') as csvfile:
        column_names = ["gameID", "player", "pokemon1", "pokemon2", "pokemon3", "pokemon4", "pokemon5", "pokemon6", "win"]
        writer = csv.DictWriter(csvfile, fieldnames=column_names)
        writer.writeheader()
        for l in links:
            try:
                if ('pokemonshowdown' in l['href']) or ('random' in l['href']) or ('double' in l['href']) or ('triple' in l['href']):
                    continue

                json_url = URL + l['href'] + '.json'
                print("fetching from " + json_url)
                battle_page = requests.get(json_url)
                log = json.loads(battle_page.content)["log"].split('\n')
                info_dict1 = {"gameID": l['href'], "win": False}
                count1 = 1
                info_dict2 = {"gameID": l['href'], "win": False}
                count2 = 1
                for row in log:
                    if row.startswith("|player|p1|"):
                        row = row[len("|player|p1|"):]
                        row = row[:row.index('|')]
                        info_dict1["player"] = row
                    elif row.startswith("|player|p2|"):
                        row = row[len("|player|p2|"):]
                        row = row[:row.index('|')]
                        info_dict2["player"] = row
                    elif row.startswith("|poke|p1|"):
                        row = row[len("|poke|p1|"):]
                        if '|' in row:
                            row = row[:row.index('|')]
                        info_dict1["pokemon" + str(count1)] = row
                        count1 += 1
                    elif row.startswith("|poke|p2|"):
                        row = row[len("|poke|p2|"):]
                        if '|' in row:
                            row = row[:row.index('|')]
                        info_dict2["pokemon" + str(count1)] = row
                        count2 += 1
                    elif row.startswith("|win|"):
                        row = row[len("|win|"):]
                        if row == info_dict1["player"]:
                            info_dict1["win"] = True
                        elif row == info_dict2["player"]:
                            info_dict2["win"] = True
                        else:
                            raise ValueError

                print("done writing data for " + json_url)
                writer.writerow(info_dict1)
                writer.writerow(info_dict2)
            except:
                pass
    
    print("Done running at " + now_str + ", sleeping for 10 mins\n")
    time.sleep(600)
    
