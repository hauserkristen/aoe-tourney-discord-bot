# External imports
import discord

# Internal imports
from db import post_tourney, Tournament

def setup_tourney(user_name: str, password: str, message: discord.Message):
    tourney_name = message.content.split('tournament')[-1].strip()
    tourney = Tournament(tourney_name, message.guild.name)
    post_tourney(user_name, password, tourney)
    return