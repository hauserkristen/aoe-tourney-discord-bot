# External imports
import os
from dotenv import load_dotenv

# Internal imports
from db import create_settings, get_guild_tourneys, delete_guild_tourneys
from db.db_connect import database_connect
from db.settings_service import _find_tourney_settings
from db.utils import Tournament

load_dotenv()
DB_USER_NAME = os.getenv('DB_USER_NAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')


def main():
    #create_settings(DB_USER_NAME, DB_PASSWORD)

    print(get_guild_tourneys(DB_USER_NAME, DB_PASSWORD, 'Test Server'))
    
    # Connect to DB
    client = database_connect(DB_USER_NAME, DB_PASSWORD)
    tourney_info = Tournament('Test Tournament', 'Test Server')
    tourney_settings = _find_tourney_settings(client, tourney_info)
    print(tourney_settings)
    client.close()


if __name__ == '__main__':
    main()