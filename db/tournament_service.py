# Internal Includes
from .db_connect import database_connect, convert_to_df
from .utils import Tournament

def post_tourney(user_name: str, password: str, tourney_info: Tournament):
    # Connect to DB
    client = database_connect(user_name, password)

    # Get database
    database = client['aoe-game-bot']

    # Add tourney to tourney table
    tbl_tourney = database['tournaments']
    if tourney_info.validate():
        tbl_tourney.insert_one(tourney_info.to_dict())

    client.close()
    return

def delete_tourney(user_name: str, password: str, tourney_info: Tournament):
    # Connect to DB
    client = database_connect(user_name, password)

    # Get database
    database = client['aoe-game-bot']

    # Get tables
    tbl_tournaments = database['tournaments']
    tbl_tourney_settings = database['tourney_settings']
    tbl_sets = database['sets']
    tbl_maps = database['maps']
    tbl_games = database['games']
    tbl_participants = database['participants']

    # Get tournament ID
    tourney_id = convert_to_df(tbl_tournaments, tourney_info.to_dict)['_id']

    # Query for rest of deletions
    id_query = {'_id' : tourney_id}

    # Drop from tables
    tbl_tournaments.delete_one(id_query)
    tbl_tourney_settings.delete_many(id_query)
    tbl_sets.delete_many(id_query)
    tbl_maps.delete_many(id_query)
    tbl_games.delete_many(id_query)
    tbl_participants.delete_many(id_query)


    client.close()
    return