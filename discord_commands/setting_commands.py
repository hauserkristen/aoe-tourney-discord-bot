# External imports
import discord

# Internal imports
from db import post_tourney_setting
from db.utils import Tournament

def save_settings(user_name: str, password: str, message: discord.Message, setting_name: str):
    # Parse setting value, validate and format as string
    setting_value = message.content.split(setting_name)[-1].strip()
    frmt_setting_value = '' # TODO
    tourney_name = '' # TODO

    # Create tourney info object
    tourney_info = Tournament(tourney_name, message.guild.name)

    post_tourney_setting(user_name, password, tourney_info, setting_name, frmt_setting_value)
    return