# External imports
import os
from dotenv import load_dotenv

# Internal imports
from db import create_settings, get_settings

load_dotenv()
DB_USER_NAME = os.getenv('DB_USER_NAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')


def main():
    create_settings(DB_USER_NAME, DB_PASSWORD)

if __name__ == '__main__':
    main()