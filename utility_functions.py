from hashlib import md5


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
