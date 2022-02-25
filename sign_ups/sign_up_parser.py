# External Includes
from re import findall
from parse import parse

# Internal Includes
from constants import *
from db import Participant

def get_elo(str: str):
    array = findall('[0-9]+', str)
    if len(array) > 0:
        return clean_string(array[0])
    else:
        return 'None'

def clean_string(str: str):
    str_enc = str.encode('ascii', 'ignore')
    str_dec = str_enc.decode()

    return str_dec.strip()

def parse_sign_up(message: str):
    # Parse fields
    discord_name = findall(DISCORD_NAME_FRMT, message)
    in_game_name = findall(IN_GAME_NAME_FRMT, message)
    profile_link = findall(PROFILE_LINK_FRMT, message)
    current_elo = findall(CURRENT_ELO_FRMT, message)
    max_elo = findall(MAX_ELO_FRMT, message)

    # Optional fields
    alt_accounts = findall(ALT_FRMT, message)

    # Check alts for profile
    if len(profile_link) == 0:
        profile_link = findall(PROFILE_LINK_ALT_FRMT, message)
        if len(profile_link) == 0:
            profile_link = findall(PROFILE_LINK_ALT2_FRMT, message)
            if len(profile_link) == 0:
                profile_link = findall(PROFILE_LINK_ALT3_FRMT, message)
                if len(profile_link) == 0:
                    profile_link = findall(PROFILE_LINK_ALT4_FRMT, message)

    # Check alts for discord name
    if len(discord_name) == 0:
        discord_name = findall(DISCORD_NAME_ALT_FRMT, message)
        if len(discord_name) == 0:
            discord_name = findall(DISCORD_NAME_ALT2_FRMT, message)

    # Check alts for in game name
    if len(in_game_name) == 0:
        in_game_name = findall(IN_GAME_NAME_ALT_FRMT, message)
        if len(in_game_name) == 0:
            in_game_name = findall(IN_GAME_NAME_ALT2_FRMT, message)
            if len(in_game_name) == 0:
                in_game_name = findall(IN_GAME_NAME_ALT3_FRMT, message)

    # Create error message if missing critical informaton
    if len(discord_name) == 0:
        error_message = 'TODO'
        return None, error_message
    elif len(in_game_name) == 0:
        error_message = 'TODO'
        return None, error_message
    elif len(profile_link) == 0:
        error_message = 'TODO'
        return None, error_message

    # Get URI
    profile_uri = clean_string(profile_link[0])

    # Create registration object
    reg = Participant()
    reg.discord_name = clean_string(discord_name[0])
    if type(in_game_name[0]) == str:
        reg.in_game_name = clean_string(in_game_name[0])
    else:
        reg.in_game_name = clean_string(in_game_name[0][-1])
    
    # Add alt accounts if included
    if len(alt_accounts) > 0:
        reg.alt_accounts = clean_string(alt_accounts[0])
    else:
        reg.alt_accounts = 'None'

    # Add current elo if included
    if len(current_elo) > 0:
        reg.reported_current_elo = get_elo(current_elo[0])
    else:
        reg.reported_current_elo = 'Not Reported'

    # Add max elo if included
    if len(max_elo) > 0:
        reg.reported_max_elo = get_elo(max_elo[0])
    else:
        reg.reported_current_elo = 'Not Reported'

    # Parse profile ID
    profile_id = 0
    if 'aoenexus' in profile_uri:
        NEXUS_FRMT = 'https://aoenexus.com/profile/#{profile_id}-{extra_num}'
        profile_id = parse(NEXUS_FRMT, profile_uri)
    elif 'aoe2.net' in profile_uri:
        AOEDOTNET_FRMT = 'https://aoe2.net/#profile-{profile_id}'
        profile_id = parse(AOEDOTNET_FRMT, profile_uri)
    elif 'aoe2insights' in profile_uri:
        INSIGHTS_FRMT = 'https://www.aoe2insights.com/user/{profile_id}/'
        profile_id = parse(INSIGHTS_FRMT, profile_uri)

    # Record
    if 'profile_id' in profile_id.named.keys():
        reg.aoe2_net_id = profile_id['profile_id']
    else:
        error_message = 'TODO'
        return None, error_message

    return reg, None

