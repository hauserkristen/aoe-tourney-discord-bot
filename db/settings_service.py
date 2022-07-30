# External Includes
from pymongo import MongoClient
import json
from typing import Any

# Internal Includes
from .db_connect import database_connect, convert_to_df

def post_tourney_setting(user_name: str, password: str, setting_name: str, setting_value: Any):
    # Connect to DB
    client = database_connect(user_name, password)

    # Get database
    database = client['aoe-game-bot']

    # Add settings to tourney settings table
    tbl_tourney_settings = database['tourney_settings']

    # TODO

    client.close()
    return

def _find_tourney_settings(client: MongoClient, guild_name: str):
    # Get database
    database = client['aoe-game-bot']

    # Get tables
    tbl_tournaments = database['tournaments']
    tbl_tourney_settings = database['tourney_settings']

    # Get tournament ID
    tourney_id = convert_to_df(tbl_tournaments, {'discord_name' : guild_name})['_id']

    # Query for settings
    tourney_settings = convert_to_df(tbl_tourney_settings, {'tournament_id': tourney_id})

    return tourney_settings

def _find_setting_id(client: MongoClient, setting_name: str):
    # Get database
    database = client['aoe-game-bot']

    # Get tables
    tbl_settings = database['settings']

    # Get tournament ID
    setting_id = convert_to_df(tbl_settings, {'name' : setting_name})['_id']

    return setting_id

def get_tourney_channels(user_name: str, password: str, guild_name: str):
    # Connect to DB
    client = database_connect(user_name, password)

    # Get tourney settings
    tourney_settings = _find_tourney_settings(client, guild_name)

    # Get rec channel setting ID
    rec_channel_id = _find_setting_id(client, 'rec_channels')
    sign_up_channel_id = _find_setting_id(client, 'sign_up_channel')

    # Query for settings
    rec_setting = convert_to_df(tourney_settings, {'setting_id': rec_channel_id})
    sign_up_setting = convert_to_df(tourney_settings, {'setting_id': sign_up_channel_id})

    # Split rec setting
    rec_channels = rec_setting['value'].split(',')
    sign_up_channel = sign_up_setting['value']

    client.close()

    # Create output map
    output = {}
    output[sign_up_channel] = 'sign_up'
    for r_c in rec_channels:
        output[r_c] = 'game_rec'

    return output

def get_tourney_summary_channel(user_name: str, password: str, guild_name: str):
    # Connect to DB
    client = database_connect(user_name, password)

    # Get tourney settings
    tourney_settings = _find_tourney_settings(client, guild_name)

    # Get rec channel setting ID
    rec_channel_id = _find_setting_id(client, 'summary_channel')

    # Query for settings
    setting = convert_to_df(tourney_settings, {'setting_id': rec_channel_id})
    setting_value = setting['value']

    client.close()

    return setting_value

def get_tourney_games_per_stage(user_name: str, password: str, guild_name: str):
    # Connect to DB
    client = database_connect(user_name, password)

    # Get tourney settings
    tourney_settings = _find_tourney_settings(client, guild_name)

    # Get rec channel setting ID
    games_per_stage_id = _find_setting_id(client, 'games_per_stage')

    # Query for settings
    setting = convert_to_df(tourney_settings, {'setting_id': games_per_stage_id})
    setting_value = setting['value']

    # Convert to dict from JSON
    setting_value = json.loads(setting_value)

    client.close()

    return setting_value

def get_tourney_map_pool(user_name: str, password: str, guild_name: str):
    # Connect to DB
    client = database_connect(user_name, password)

    # Get database
    database = client['aoe-game-bot']

    # Get tables
    tbl_tournaments = database['tournaments']
    tbl_maps = database['maps']

    # Get tournament ID
    tourney_id = convert_to_df(tbl_tournaments, {'discord_name' : guild_name})['_id']

    # Get map names 
    maps = convert_to_df(tbl_maps, {'tournament_id': tourney_id})
    map_values = []
    for m in maps:
        map_values.append(m['name'])

    client.close()

    return map_values

def delete_settings():
    # TODO
    pass

def create_settings(user_name: str, password: str):
    client = database_connect(user_name, password)

    # Get database
    database = client['aoe-game-bot']

    # Get collections
    tbl_settings = database['settings']

    # Set up global settings
    tbl_settings.insert_many([
        {"name": "rec_channels"},
        {"name": "summary_channel"},
        {"name": "sign_up_channel"},
        {"name": "games_per_stage"}
    ])
    return

def get_settings(user_name: str, password: str):
    client = database_connect(user_name, password)

    # Get database
    database = client['aoe-game-bot']

    # Get collections
    tbl_settings = database['settings']

    # Get global settings 
    return convert_to_df(tbl_settings, columns={'name': 1, '_id': 0})
