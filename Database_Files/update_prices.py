import sqlite3
import pandas as pd

connection = sqlite3.connect('main_database.db')
cursor = connection.cursor()
default = pd.read_csv('default.csv')

for row in default.iterrows():
    scryfall = row[1]['scryfall_uri']
    usd = row[1]['usd']
    usd_foil = row[1]['usd_foil']
    query = "update all_entries set usd = '{0}', usd_foil = '{1}' where scryfall_uri = '{2}'"
    cursor.execute(query.format(usd, usd_foil, scryfall))
connection.commit()
connection.close()
