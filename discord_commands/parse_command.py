# External imports
import discord

# Internal imports
from db import get_settings
from .tourney_commands  import setup_tourney
from .setting_commands import save_settings
from .set_comamnds import log_admin_win

def parse_command(user_name: str, password: str, message: discord.Message):
    # TODO: Check for admin user

    # Check for setup commands
    if message.content.startswith('!setup'):
        # Parse setup field
        field =  message.content.split(' ')[1].lower()

        # Get setting names
        setting_names = get_settings(user_name, password)['name']

        # Setup Tourney
        if field == 'tournament':
            setup_tourney(user_name, password, message)
        # Settings Configuration
        elif field in setting_names.values:
            save_settings(user_name, password, message, field)
    # Check for Admin W/L
    elif message.content.startswith('!admin_win'):
        log_admin_win(user_name, password, message)

    return