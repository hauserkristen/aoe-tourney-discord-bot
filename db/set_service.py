# Internal Includes
from .db_connect import database_connect
from .utils import GameSet

def post_set(user_name: str, password: str, game_set: GameSet, guild_name: str):
    # Connect to DB
    client = database_connect(user_name, password)

    # Get database
    database = client['aoe-game-bot']

    # Get tables
    tbl_tournaments = database['tournaments']
    tbl_participants = database['participants']
    tbl_sets = database['sets']
    tbl_games = database['games']
    tbl_maps = database['games']

    # Get tournament ID
    tourney_id = tbl_tournaments.find({'discord_name' : guild_name})['_id']

    # Get player IDs
    p1_id = tbl_participants.find({'tournament_id' : tourney_id, 'name': game_set.p1_name})['_id']
    p2_id = tbl_participants.find({'tournament_id' : tourney_id, 'name': game_set.p2_name})['_id']

    # Add set to set table
    if game_set.validate():
        tbl_sets.insert_one(game_set.to_dict(tourney_id, p1_id, p2_id))

    # Get set ID
    set_id = tbl_sets.find({'tournament_id' : tourney_id, 'p1_id': p1_id, 'p2_id': p2_id, 'stage': game_set.stage})['_id']

    for g in game_set:
        if g.validate():
            # Get other IDs
            map_id = tbl_maps.find({'tournament_id' : tourney_id, 'name': g.map})['_id']
            winner_id = tbl_participants.find({'tournament_id' : tourney_id, 'name': g.winner})['_id']

            tbl_games.insert_one(g.to_dict(set_id, map_id, winner_id))

    client.close()
    return

def delete_set(user_name: str, password: str, guild_name: str, p1_name: str, p2_name: str, stage: str):
    # Connect to DB
    client = database_connect(user_name, password)

    # Get database
    database = client['aoe-game-bot']

    # Get tables
    tbl_tournaments = database['tournaments']
    tbl_participants = database['participants']
    tbl_sets = database['sets']
    tbl_games = database['games']

    # Get tournament ID
    tourney_id = tbl_tournaments.find({'discord_name' : guild_name})['_id']

    # Get player IDs
    p1_id = tbl_participants.find({'tournament_id' : tourney_id, 'name': p1_name})['_id']
    p2_id = tbl_participants.find({'tournament_id' : tourney_id, 'name': p2_name})['_id']

    # Get set ID
    set_id = tbl_sets.find({'tournament_id' : tourney_id, 'p1_id': p1_id, 'p2_id': p2_id, 'stage': stage})['_id']

    # Delete by query
    tbl_sets.delete_one({'tournament_id': tourney_id, '_id': set_id})
    tbl_games.delete_many({'tournament_id': tourney_id, 'set_id': set_id})

    client.close()
    return

def get_set():
    # TODO
    pass
