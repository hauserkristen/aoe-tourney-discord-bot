from pymongo import MongoClient
from pandas import DataFrame
import certifi

def database_connect(user_name: str, password: str):
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(
        host='mongodb+srv://aoe-game-bot.6ltkx.mongodb.net',
        username=user_name,
        password=password,
        tlsCAFile=certifi.where()
    )

    # Create the database for our example (we will use the same database throughout the tutorial
    return client

def convert_to_df(mongo_collection, query={}, columns=None):
    cursor = mongo_collection.find(query, columns)
    list_cur = list(cursor)
    if not list_cur:
        return []
    elif len(list_cur) > 1:
        return DataFrame(list_cur)
    else:
        return list_cur[0]
