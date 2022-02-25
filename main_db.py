# External imports
import os
from dotenv import load_dotenv

# Internal imports
from db import database_connect, convert_to_df

load_dotenv()
DB_USER_NAME = os.getenv('DB_USER_NAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')


def main():
    client = database_connect(DB_USER_NAME, DB_PASSWORD)

    # Get database
    database = client['aoe-game-bot']

    # Get collections
    tbl_settings = database['settings']

    # Set up tourney settings table
    if False:
        tbl_settings.drop()
    if False:
        tbl_settings.insert_many([
            {"name": "rec_channels"},
            {"name": "summary_channel"},
            {"name": "sign_up_channel"},
            {"name": "games_per_stage"}
        ])
    
    # Verify
    df = convert_to_df(tbl_settings)

    client.close()

if __name__ == '__main__':
    main()