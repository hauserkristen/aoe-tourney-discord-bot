# Internal Includes
from .db_connect import database_connect, convert_to_df
from .utils import Participant, Tournament

def post_participant(user_name: str, password: str, participant: Participant):
    # Connect to DB
    client = database_connect(user_name, password)

    # Get database
    database = client['aoe-game-bot']

    # Get tables
    tbl_tournaments = database['tournaments']
    tbl_participants = database['participants']

    # Get tournament ID
    tourney_id = str(convert_to_df(tbl_tournaments, participant.get_tourney())['_id'])

    # Check if participant already exists
    found_participant = tbl_participants.find_one(participant.to_dict(tourney_id))

    # Add participant to particpant table
    if found_participant is None and participant.validate():
        tbl_participants.insert_one(participant.to_dict(tourney_id))

    client.close()
    return

def get_participant(user_name: str, password: str, tourney_info: Tournament, discord_name: str):
    # Connect to DB
    client = database_connect(user_name, password)

    # Get database
    database = client['aoe-game-bot']

    # Get tables
    tbl_tournaments = database['tournaments']
    tbl_participants = database['participants']

    # Get tournament ID
    tourney_id = str(convert_to_df(tbl_tournaments, tourney_info.to_dict())['_id'])

    # Query for settings
    participant = convert_to_df(tbl_participants, {'tournament_id': tourney_id, 'discord_name': discord_name})

    client.close()

    return participant

def delete_participant(user_name: str, password: str, tourney_info: Tournament, discord_name: str):
    # Connect to DB
    client = database_connect(user_name, password)

    # Get database
    database = client['aoe-game-bot']

    # Get tables
    tbl_tournaments = database['tournaments']
    tbl_participants = database['participants']

    # Get tournament ID
    tourney_id = str(convert_to_df(tbl_tournaments, tourney_info.to_dict())['_id'])

    # Delete by query
    tbl_participants.delete_one({'tournament_id': tourney_id, 'discord_name': discord_name})

    client.close()
    return