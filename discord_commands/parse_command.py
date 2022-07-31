# External imports
import discord

# Internal imports
from db import get_settings
from .tourney_commands  import setup_tourney
from .setting_commands import save_settings
from .set_comamnds import log_admin_win
from .utils import extract_key_value_pairs, has_keys

def parse_command(user_name: str, password: str, message: discord.Message):
    # TODO: Check for tourney admin user

    # Check for setup commands
    if message.content.startswith('!help'):
        if message.content == '!help':
            # TODO: Have general help message that lists the various commands
            help_message = ''
        else:
            # Parse setup field
            field =  message.content.split(' ')[1].lower()
            if field == 'setup':
                # TODO: Explain the required format for two setup commands
                help_message = ''
            elif field == 'admin_win':
                # TODO: Explain the required format for admin win command
                help_message = ''
        return help_message
    elif message.content.startswith('!setup'):
        # Parse key value pairs
        setup_kvs_str = message.content.split('!setup')[-1].strip()
        setup_kvs = extract_key_value_pairs(setup_kvs_str)

        # Get setting names
        setting_names = get_settings(user_name, password)['name'].values

        # Setup Tourney
        if 'tournament' in setup_kvs.keys():
            setup_tourney(user_name, password, setup_kvs['tournament'], message.guild.name)
            return True
        # Settings Configuration
        if has_keys(setup_kvs.keys, setting_names, ['tournament']):
            save_settings(user_name, password, setup_kvs, setting_names, message.guild.name)
            return True
    # Check for Admin W/L
    elif message.content.startswith('!admin_win'):
        log_admin_win(user_name, password, message)
        return True

    return False