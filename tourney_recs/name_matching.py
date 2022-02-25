# External Includes
from difflib import SequenceMatcher

def match_name(name, player_one, player_two):
    # ASSUMPTION: Name in score is same or similar to in game name. Reporting discord name can be anything.

    # Exact match cases
    if name == player_one:
        return player_one
    elif name == player_two:
        return player_two

    # Not an exact match
    player_one_score = SequenceMatcher(None, name, player_one).ratio()
    player_two_score = SequenceMatcher(None, name, player_two).ratio()

    if player_one_score > player_two_score:
        return player_one
    else:
        return player_two


def estimate_host_and_guest(host_name, guest_name, player_one, player_two):
    # ASSUMPTION: One name in score is same or similar to in game name. Reporting discord name can be anything.
    host_name_l = host_name.lower()
    guest_name_l = guest_name.lower()
    player_one_l = player_one.lower()
    player_two_l = player_two.lower()

    # Exact match cases
    if host_name_l == player_one_l:
        return player_one, player_two
    elif host_name_l == player_two_l:
        return player_two, player_one
    elif guest_name_l == player_one_l:
        return player_two, player_one
    elif guest_name_l == player_two_l:
        return player_one, player_two

    # Not an exact match
    player_one_host_score = SequenceMatcher(None, host_name_l, player_one_l).ratio()
    player_two_host_score = SequenceMatcher(None, host_name_l, player_two_l).ratio()
    player_one_guest_score = SequenceMatcher(None, guest_name_l, player_one_l).ratio()
    player_two_guest_score = SequenceMatcher(None, guest_name_l, player_two_l).ratio()
    all_scores = [player_one_host_score, player_two_host_score, player_one_guest_score, player_two_guest_score]

    if player_one_host_score == max(all_scores):
        return player_one, player_two
    elif player_two_host_score == max(all_scores):
        return player_two, player_one
    elif player_one_guest_score == max(all_scores):
        return player_two, player_one
    else:
        return player_one, player_two