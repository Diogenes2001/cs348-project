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
    if os.path.isfile('../hello-world/src/assets/pokemon/{0}.png'.format(id)): # if already have image, no need to get another one
        print("image exists for pokemon {0}: {1}".format(id, name))
        skipped.append(id)
        continue
    print("getting image for pokemon {0}: {1}".format(id, name))
    try:
        filename = 'File:{0:03d}{1}.png'.format(id, name)
        URL = 'https://bulbapedia.bulbagarden.net/wiki/' + filename
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        img = soup.find('img', alt=filename)
        with open('../hello-world/src/assets/pokemon/{0}.png'.format(id), 'wb') as handler:
            img_location = img.attrs['src']
            if not img_location.startswith("https:"):
                img_location = "https:" + img_location
            response = requests.get(img_location, stream=True)
            handler.write(response.content)
    except:
        print("failed to get image for pokemon {0}: {1}".format(id, name))
        failed.append(id)

msg = "pokemon skipped: " + ','.join(skipped) + "\npokemon failed: " + ','.join(failed)
print(msg)
with open('image_scraper.log', 'wb') as handler:
    handler.write(msg)