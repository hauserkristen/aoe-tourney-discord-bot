# External imports
import discord

# Internal imports
from db import post_admin_win
from db.utils import Tournament

def log_admin_win(user_name: str, password: str, message: discord.Message):
    # TODO: Extract required params
    tourney_name = ''
    winner_name = '' 
    loser_name = ''
    stage = ''

    # Create tourney info object
    tourney_info = Tournament(tourney_name, message.guild.name)

    post_admin_win(user_name, password, tourney_info, winner_name, loser_name, stage)
    return