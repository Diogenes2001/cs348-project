import requests
from bs4 import BeautifulSoup
import json
import csv
import datetime
import string
import time
import json
import psycopg2
import os

# connect to the database
conn = psycopg2.connect(host="localhost",
    database="Flask", user="postgres", password="password")
cur = conn.cursor()

cur.execute(
    '''
    SELECT id, name
    FROM Pokemon
    '''
)
failed = []
skipped = []
for id, name in cur:
    filename = '../hello-world/src/assets/pokemon/{0}-shiny.png'.format(id)
    if os.path.isfile(filename): # if already have image, no need to get another one
        print("image exists for pokemon {0}: {1}".format(id, name))
        skipped.append(str(id))
        continue
    print("getting image for pokemon {0}: {1}".format(id, name))
    try:
        with open(filename, 'wb') as handler:
            img_location = 'https://www.serebii.net/Shiny/SWSH/{0:03d}.png'.format(id)
            response = requests.get(img_location, stream=True)
            handler.write(response.content)
    except:
        print("failed to get image for pokemon {0}: {1}".format(id, name))
        if os.path.exists(filename):
            os.remove(filename)
        failed.append(str(id))

msg = "pokemon skipped: " + ','.join(skipped) + "\npokemon failed: " + ','.join(failed)
print(msg)
f = open("image_scraper.log", "w")
f.write(msg)
f.close()