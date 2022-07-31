from typing import List


def extract_key_value_pairs(input_string: str):
    kvs = dict(item.split('=') for item in input_string.split(', '))

    sanitized_kvs = {}
    for k, v in kvs.items():
        sanitized_kvs[k.strip()] = v.strip().strip('\"')

    return sanitized_kvs

def has_keys(input_keys: List[str], search_keys: List[str], required_keys: List[str] = []):
    for  i_key in input_keys:
        if i_key in search_keys:
            return True and set(required_keys).issubset(set(input_keys))
    return False