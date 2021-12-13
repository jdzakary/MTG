from requests import get
import json
import pandas as pd
from ast import literal_eval
from os import remove


def parse_default(input_string, target):
    try:
        return literal_eval(input_string)[target]
    except ValueError:
        return None


def parse_oracle(input_string, target):
    this_value = literal_eval(input_string)[target]
    if this_value == 'not_legal':
        return False
    elif this_value == 'legal':
        return True


def data_download(path_prefix: str):
    ######
    # Downloading New JSON Files
    ######
    general_url = 'https://api.scryfall.com/bulk-data'
    with get(general_url, stream=True) as download:
        with open(f'{path_prefix}temp.json', 'wb') as file:
            for chunk in download.iter_content():
                file.write(chunk)
    oracle_url = ''
    default_url = ''
    with open(f'{path_prefix}temp.json', 'r') as file:
        directions = json.load(file)
    for item in directions['data']:
        if item['type'] == 'oracle_cards':
            oracle_url = item['download_uri']
        elif item['type'] == 'default_cards':
            default_url = item['download_uri']
    with get(oracle_url, stream=True) as download:
        with open(f'{path_prefix}oracle.json', 'wb') as file:
            for chunk in download.iter_content(chunk_size=16*1024):
                file.write(chunk)
    with get(default_url, stream=True) as download:
        with open(f'{path_prefix}default.json', 'wb') as file:
            for chunk in download.iter_content(chunk_size=16*1024):
                file.write(chunk)

    ######
    # Convert default JSON to CSV
    ######
    default_data = pd.read_json(f'{path_prefix}default.json')
    selection = default_data[['oracle_id', 'tcgplayer_id', 'name', 'scryfall_uri', 'image_uris', 'foil', 'nonfoil', 'oversized',
                              'promo', 'set_id', 'set', 'set_name', 'set_type', 'full_art', 'textless', 'prices', 'frame_effects',
                              'promo_types', 'card_faces', 'border_color']]
    selection.to_csv(f'{path_prefix}temp.csv', index=False)
    new_default_data = pd.read_csv(f'{path_prefix}temp.csv')
    remove(f'{path_prefix}temp.csv')

    # Prices
    new_default_data['usd'] = new_default_data['prices'].apply(lambda x: parse_default(x, 'usd'))
    new_default_data['usd'].fillna(0, inplace=True)
    new_default_data['usd_foil'] = new_default_data['prices'].apply(lambda x: parse_default(x, 'usd_foil'))
    new_default_data['usd_foil'].fillna(0, inplace=True)

    # Image URL
    new_default_data['image_url_1'] = new_default_data['image_uris'].apply(lambda x: parse_default(x, 'normal'))
    new_default_data['image_url_2'] = None

    # Art and Associated
    new_default_data['extended'] = new_default_data['frame_effects'].str.contains('extendedart')
    new_default_data['extended'].fillna(False, inplace=True)
    new_default_data['showcase'] = new_default_data['frame_effects'].str.contains('showcase')
    new_default_data['showcase'].fillna(False, inplace=True)
    new_default_data['prerelease'] = new_default_data['promo_types'].str.contains('prerelease')
    new_default_data['prerelease'].fillna(False, inplace=True)
    # new_default_data['borderless'] = new_default_data['border_color'].str.contains('borderless')
    # new_default_data['borderless'].fillna(False, inplace=True)

    # Card Faces
    for row in new_default_data.iterrows():
        this_index = row[0]
        faces = row[1]['card_faces']
        if type(faces) == str:
            try:
                front_url = literal_eval(faces)[0]['image_uris']['normal']
                back_url = literal_eval(faces)[1]['image_uris']['normal']
                new_default_data.at[this_index, 'image_url_1'] = front_url
                new_default_data.at[this_index, 'image_url_2'] = back_url
            except KeyError:
                pass

    # Drop non-needed Columns
    new_default_data.drop(labels=['prices', 'frame_effects', 'promo_types', 'image_uris', 'card_faces', 'set', 'border_color'], axis=1, inplace=True)

    # Write to File
    new_default_data.to_csv(f'{path_prefix}default.csv', index=False)

    ######
    # Convert oracle JSON to CSV
    ######
    oracle_data = pd.read_json(f'{path_prefix}oracle.json')
    selection = oracle_data[['oracle_id', 'name', 'mana_cost', 'cmc', 'type_line', 'oracle_text', 'power',
                             'toughness', 'colors', 'color_identity', 'keywords', 'legalities', 'reserved', 'rulings_uri',
                             'rarity', 'flavor_text', 'edhrec_rank', 'loyalty', 'card_faces']]
    for row in selection.iterrows():
        if str(row[1]['loyalty']).isnumeric():
            pass
        elif str(row[1]['loyalty']) == 'nan':
            pass
        else:
            this_index = row[0]
            selection.at[this_index, 'loyalty'] = None
    selection['loyalty'].astype('float64')
    selection.to_csv(f'{path_prefix}temp.csv', index=False)
    new_oracle_data = pd.read_csv(f'{path_prefix}temp.csv')
    remove(f'{path_prefix}temp.csv')

    new_oracle_data.rename(columns={'oracle_text': 'oracle_text_1'}, inplace=True)
    new_default_data['oracle_text_2'] = None

    # Card Faces
    for row in new_oracle_data.iterrows():
        this_index = row[0]
        faces = row[1]['card_faces']
        if type(faces) == str:
            try:
                front_oracle = literal_eval(faces)[0]['oracle_text']
                back_oracle = literal_eval(faces)[1]['oracle_text']
                new_oracle_data.at[this_index, 'oracle_text_1'] = front_oracle
                new_oracle_data.at[this_index, 'oracle_text_2'] = back_oracle
            except KeyError:
                pass

    new_oracle_data['standard'] = new_oracle_data['legalities'].apply(lambda x: parse_oracle(x, 'standard'))
    new_oracle_data['modern'] = new_oracle_data['legalities'].apply(lambda x: parse_oracle(x, 'modern'))
    new_oracle_data['vintage'] = new_oracle_data['legalities'].apply(lambda x: parse_oracle(x, 'vintage'))
    new_oracle_data['commander'] = new_oracle_data['legalities'].apply(lambda x: parse_oracle(x, 'commander'))
    new_oracle_data.drop(labels=['legalities', 'card_faces'], axis=1, inplace=True)
    new_oracle_data.to_csv(f'{path_prefix}oracle.csv', index=False)

    ######
    # Removing JSON files that are not needed
    ######
    remove(f'{path_prefix}temp.json')
    remove(f'{path_prefix}default.json')
    remove(f'{path_prefix}oracle.json')
