# Internal imports
from db import post_tourney, Tournament

def setup_tourney(user_name: str, password: str, tourney_name: str, guild_name: str):
    tourney = Tournament(tourney_name, guild_name)
    post_tourney(user_name, password, tourney)
    return