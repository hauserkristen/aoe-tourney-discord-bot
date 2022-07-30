# Internal Includes
from .db_connect import database_connect, convert_to_df

def delete_guild_tourneys(user_name: str, password: str, guild_name: str):
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

    # Query for deletion
    name_query = {'guild_name' : guild_name}

    # Get tournament IDs
    tourney_ids = convert_to_df(tbl_tournaments, name_query)
    
    for tourney_id in tourney_ids:
        # Query for rest of deletions
        id_query = {'_id' : tourney_id['_id']}

        # Drop from tables
        tbl_tournaments.delete_one(id_query)
        tbl_tourney_settings.delete_many(id_query)
        tbl_sets.delete_many(id_query)
        tbl_maps.delete_many(id_query)
        tbl_games.delete_many(id_query)
        tbl_participants.delete_many(id_query)


    client.close()
    return