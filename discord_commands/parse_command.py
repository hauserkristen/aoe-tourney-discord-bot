# External imports
import discord

# Internal imports
from db import get_settings, post_tourney, post_tourney_setting, Tournament

def parse_command(user_name: str, password: str, message: discord.Message):
    # Check for admin user

    # Check for setup commands
    if message.content.startswith('!setup'):
        # Parse setup field
        field =  message.content.split(' ')[1].lower()

        # Setup tourney
        if field == 'tournament':
            tourney_name = message.content.split('tournament')[-1].strip()
            tourney = Tournament(tourney_name, message.guild.name)
            post_tourney(user_name, password, tourney)
        # Settings Configuration
        setting_names = get_settings(user_name, password)['name']
        if field in setting_names.values:
            setting_value = '' # TODO
            post_tourney_setting(user_name, password, field, setting_value)
        
    # Check for Admin W/L
    elif message.content.startswith('!admin_win'):
        # TODO
        pass

    return