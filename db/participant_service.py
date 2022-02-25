# Internal Includes
from .db_connect import database_connect
from .utils import Participant

def post_participant(user_name: str, password: str, participant: Participant):
    # Connect to DB
    client = database_connect(user_name, password)

    # Get database
    database = client['aoe-game-bot']

    # Add participant to particpant table
    tbl_participants = database['participants']
    if participant.validate():
        tbl_participants.insert_one(participant.to_dict())

    client.close()
    return

def get_participant(user_name: str, password: str, guild_name: str, discord_name: str):
    # Connect to DB
    client = database_connect(user_name, password)

    # Get database
    database = client['aoe-game-bot']

    # Get tables
    tbl_tournaments = database['tournaments']
    tbl_participants = database['participants']

    # Get tournament ID
    tourney_id = tbl_tournaments.find({'discord_name' : guild_name})['_id']

    # Query for settings
    participant = tbl_participants.find({'tournament_id': tourney_id, 'discord_name': discord_name})

    client.close()

    return participant

def delete_participant(user_name: str, password: str, guild_name: str, discord_name: str):
    # Connect to DB
    client = database_connect(user_name, password)

    # Get database
    database = client['aoe-game-bot']

    # Get tables
    tbl_tournaments = database['tournaments']
    tbl_participants = database['participants']

    # Get tournament ID
    tourney_id = tbl_tournaments.find({'discord_name' : guild_name})['_id']

    # Delete by query
    tbl_participants.delete_one({'tournament_id': tourney_id, 'discord_name': discord_name})

    client.close()
    return