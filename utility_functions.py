from hashlib import md5
import pandas as pd
import sqlalchemy as db


def contains_any(input_string: str, input_set: list):
    for character in input_set:
        if character in input_string: return True
    return False


def fetch_image(set_type: str, set_name: str, card_id: str, back: bool = False) -> bytes:
    hash_type = md5(set_type.encode()).hexdigest()
    hash_name = md5(set_name.encode()).hexdigest()
    hash_id = md5(card_id.encode()).hexdigest()
    if back:
        filepath = f'/Laptop DATA No Transfer/MTG Image Database/{hash_type}/{hash_name}/{hash_id}_back.png'
    else:
        filepath = f'/Laptop DATA No Transfer/MTG Image Database/{hash_type}/{hash_name}/{hash_id}.png'
    with open(filepath, 'rb') as file1:
        image_data = file1.read()
    return image_data


def fetch_graph(collection_name: str, file_name: str) -> bytes:
    filepath = f'Graphs/PNG/{collection_name}/{file_name}.png'
    with open(filepath, 'rb') as file:
        image_data = file.read()
    return image_data


def graph_data(target_collection: str, path_prefix: str) -> pd.DataFrame:
    engine = db.create_engine(f'sqlite:///{path_prefix}Database_Files/main_database.db')
    with open(f'{path_prefix}Database_Files/SQL_Files/collection_data.sql', 'r') as file:
        query = file.read()
    query = query.replace('collection_1', target_collection)
    data = pd.read_sql(query, engine)
    return data
