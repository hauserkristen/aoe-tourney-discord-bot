# External imports
from requests import get
from re import findall
from typing import List, Dict

# Internal imports
from db import GameSet
from constants import *
from .name_matching import estimate_host_and_guest

def parse_discord_message(message: str, tourney_map_pool: List[str], games_per_stage: Dict[str, int]):
    game_set = GameSet()

    # Parse string
    stage = findall(STAGE_FRMT, message)
    civ_draft = findall(CIV_DRAFT_FRMT, message)
    maps = findall(SELECTED_MAPS_FRMT, message)
    score =  findall(SCORE_FRMT, message)

    # Check for alt usage
    if len(score) == 0 or (len(score) > 0 and len(score[0]) < 5):
        score =  findall(SCORE_ALT_FRMT, message)

    # Check if no fields were found, probably just a chatty message
    pass_message = all([
        len(stage) == 0,
        len(civ_draft) == 0,
        len(maps) == 0,
        len(score) == 0
    ])
    if pass_message:
        return game_set, [], None, False

    # Check spoiler tag was used
    spoiler_count = message.count('||')
    if spoiler_count == 0:
        error_message = 'The recently submitted set does not meet format due because no spoiler tag was found. Please check sample and correct submission. Thank you'
        return game_set, [], error_message, False

    # Check all were found
    if len(stage) == 0:
        error_message = 'The recently submitted set does not meet format due to missing or incomplete field: Stage. Please check sample and correct submission. Thank you'
        return game_set, [], error_message, False
    else:
        game_set.stage = parse_stage(stage[0].strip(), games_per_stage)

        # Error handling for unknown stage
        if game_set.stage == -1:
            error_message = 'The recently submitted set does not meet format due to missing or incomplete field: Stage. Found an unknown string ({}), valid strings are ({}). Please check sample and correct submission. Thank you'.format(stage[0].strip(), ','.join(STR_TO_STAGE.keys()))
            return game_set, [], error_message, False
        elif game_set.stage == 0:
            error_message = 'The recently submitted set does not meet format due to missing or incomplete field: Stage. Found an unknown int ({}), valid ints are ({}). Please check sample and correct submission. Thank you'.format(stage[0].strip(), ','.join(games_per_stage.keys()))
            return game_set, [], error_message, False

    if len(maps) == 0:
        error_message = 'The recently submitted set does not meet format due to missing or incomplete field: Maps, it is likely you are missing HM notation. Please check sample and correct submission. Thank you'
        return game_set, [], error_message, False
    else:
        # Get maps from map pool
        # TODO: Accomodate CM map drafting
        available_maps = []
        for m in maps:
            for p_m in m.strip().split(','):
                available_maps.append(p_m)

        # Ensure each one is in the valid map list
        # TODO: Would not need to validate if using CM
        for i in range(len(available_maps)):
            i_map = available_maps[i]
            if i_map not in tourney_map_pool:
                error_message = 'The recently submitted set has a map mismatch, {} was played but not in the map pool ({}). Please check sample and correct submission. Thank you'.format(i_map, ','.join(tourney_map_pool))
                return game_set, available_maps, error_message, False

    if len(score) == 0 or (len(score) > 0 and len(score[0]) < 3):
        error_message = 'The recently submitted set does not meet format due to missing or incomplete field: Score. Please check sample and correct submission. Thank you'
        return game_set, available_maps, error_message, False
    else:
        score = score[0]
        game_set.p1_reported_score = int(score[1])
        game_set.p2_reported_score = int(score[-2])

        # Get player names
        game_set.p1_name = score[0].strip()
        game_set.p2_name = score[-1].strip()

    if len(civ_draft) == 0:
        error_message = 'The recently submitted set does not meet format due to missing or incomplete field: Civ Draft. Please check sample and correct submission. Thank you'
        return game_set, available_maps, error_message, False
    else:
        # Get civ draft
        civ_draft_uri= civ_draft[0].strip()
        index = civ_draft_uri.index('/draft')
        api_uri = civ_draft_uri[:index] + '/api' + civ_draft_uri[index:]
        civ_draft_response = get(api_uri)
        civ_draft_json = civ_draft_response.json()

        # Map names
        host_name, guest_name = estimate_host_and_guest(civ_draft_json['nameHost'], civ_draft_json['nameGuest'], game_set.p1_name, game_set.p2_name)

        # Parse civ draft
        player_map = {
            'HOST': host_name,
            'GUEST': guest_name
        }
        for event in civ_draft_json['events']:
            if event.get('actionType') == 'pick':
                # Get player name
                if player_map[event['player']] == game_set.p1_name:
                    game_set.p1_available_civs.append(event['chosenOptionId'])
                else:
                    game_set.p2_available_civs.append(event['chosenOptionId'])
            elif event.get('actionType') == 'snipe':
                if player_map[event['player']] == game_set.p1_name:
                    game_set.p2_available_civs.remove(event['chosenOptionId'])
                else:
                    game_set.p1_available_civs.remove(event['chosenOptionId'])
            elif event.get('actionType') == 'steal':
                if player_map[event['player']] == game_set.p1_name:
                    game_set.p2_available_civs.remove(event['chosenOptionId'])
                    game_set.p1_available_civs.append(event['chosenOptionId'])
                else:
                    game_set.p1_available_civs.remove(event['chosenOptionId'])
                    game_set.p2_available_civs.append(event['chosenOptionId'])

    return game_set, available_maps, None, True

def parse_stage(stage_str: str, games_per_stage: Dict[str, int]):
    if stage_str in STR_TO_STAGE.keys():
        return STR_TO_STAGE[stage_str]
    elif stage_str.isnumeric():
        try:
            stage_int = int(stage_str)
            if stage_int not in games_per_stage.keys():
                return 0
            else:
                return stage_int
        except ValueError:
            return 0
    else:
        return -1
