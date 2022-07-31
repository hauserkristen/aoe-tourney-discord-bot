# External imports
import discord

# Internal imports
from db import post_admin_win
from db.utils import Tournament
from .utils import extract_key_value_pairs

REQUIRED_KEYS = ['tourney_name', 'winner_name', 'loser_name', 'stage']

# Format Ex: !admin_win tourney_name="Test Tourney", winner_name="Stealth_R_Us", loser_name="paradox303", stage="Ro16"
def log_admin_win(user_name: str, password: str, message: discord.Message):
    # Parse key value pairs
    admin_win_kvs_str = message.content.split('!admin_win')[-1].strip()
    admin_win_kvs = extract_key_value_pairs(admin_win_kvs_str)

    # Extract required params
    if set(REQUIRED_KEYS).issubset(set(admin_win_kvs)):
        # Create tourney info object
        tourney_info = Tournament(admin_win_kvs['tourney_name'], message.guild.name)

        post_admin_win(
            user_name,
            password,
            tourney_info,
            admin_win_kvs['winner_name'],
            admin_win_kvs['loser_name'],
            admin_win_kvs['stage']
        )
    return