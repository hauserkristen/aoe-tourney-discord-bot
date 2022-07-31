# External imports
from typing import Dict, List

# Internal imports
from db import post_tourney_setting
from db.utils import Tournament

# TODO: Concern about formamtting here since if there are spaces between commas, everything will get weird
# rec_channels - csv str, Ex: !setup rec_channels="Rec Channel1,Rec Channel2,Rec Channel3"
# summary_channel - str, Ex: !setup summary_channel="Summary Channel"
# sign_up_channel - str, Ex: !setup sign_up_channel="Sign Up Channel"
# games_per_stage - json { str: int }, Ex: !setup games_per_stage="Ro16=3,Ro8=5,Semis=5,Finals=7"
def save_settings(user_name: str, password: str, setup_kvs: Dict[str, str], available_setting_names: List[str], guild_name: str):
    # Create tourney info object
    tourney_info = Tournament(setup_kvs['tournament'], guild_name)

    # Save settings
    for setting_name, setting_value in setup_kvs.items():
        if setting_name in available_setting_names:
            post_tourney_setting(user_name, password, tourney_info, setting_name, setting_value)
    return

