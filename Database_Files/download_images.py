import pandas as pd
import requests as req
import sqlite3
from os import chdir, makedirs
import hashlib
import requests.exceptions


def download_images(path_prefix: str):
    connection = sqlite3.connect(f'{path_prefix}main_database.db')
    cursor = connection.cursor()
    with open(f'{path_prefix}SQL_Files/image_query.sql', 'r') as file:
        query = file.read()
    proxy = cursor.execute(query)
    results = pd.DataFrame(proxy.fetchall(), columns=['set_type', 'set_name', 'type_line', 'scryfall', 'url_1', 'url_2'])

    chdir("C:\\Laptop DATA No Transfer\\MTG Image Database")
    for row in results.iterrows():
        card_id = hashlib.md5(row[1]['scryfall'].encode()).hexdigest()
        set_name = hashlib.md5(row[1]['set_name'].encode()).hexdigest()
        set_type = hashlib.md5(row[1]['set_type'].encode()).hexdigest()
        filepath = '{0}/{1}/'.format(set_type, set_name)
        try:
            makedirs(filepath)
        except FileExistsError:
            pass
        if row[1]['url_1'] != None:
            try:
                image_request = req.get(row[1]['url_1'])
                with open('{0}/{1}.png'.format(filepath, card_id), 'wb') as file:
                    file.write(image_request.content)
                cursor.execute("update all_entries set downloaded = TRUE where scryfall_uri = '{0}'".format(row[1]['scryfall']))
                connection.commit()
            except requests.exceptions.HTTPError:
                pass
        if row[1]['url_2'] != None:
            try:
                image_back = req.get(row[1]['url_2'])
                card_id = hashlib.md5((row[1]['scryfall'] + 'Back').encode()).hexdigest()
                with open('{0}/{1}_back.png'.format(filepath, card_id), 'wb') as file:
                    file.write(image_back.content)
            except requests.exceptions.HTTPError:
                pass
