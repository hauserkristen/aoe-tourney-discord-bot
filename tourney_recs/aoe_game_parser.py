# External Includes
import os
import shutil
from typing import List
from parse import parse
from mgz.reference import get_dataset
from mgz.util import Version
from mgz.summary import Summary
from discord.file import File
from zipfile import ZipFile
from pathlib import Path

# Internal Includes
from constants import *
from db import Game, GameSet
from .name_matching import match_name

def parse_zipped_game_files(zipped_filepath: str,  game_set: GameSet, available_maps: List[str], num_games: int):
    # Get extraction location
    zipped_filepath = Path(zipped_filepath)
    zip_directory = zipped_filepath.parent
    zip_destination = zip_directory.joinpath(zipped_filepath.stem)
    
    # Download and unzip
    with ZipFile(zipped_filepath,"r") as zip_ref:
        zip_ref.extractall(zip_destination)

    # Get file names
    game_filepaths = [os.path.join(dp, f) for dp, dn, filenames in os.walk(zip_destination) for f in filenames if Path(f).suffix == '.aoe2record']
    game_filenames = [Path(f).name for f in game_filepaths]

    # Parse
    game_set, error_message = parse_game_files(game_filenames, game_filepaths, game_set, available_maps, num_games)

    # Remove destination directory and zip
    if zip_destination.exists() and zip_destination.is_dir():
        shutil.rmtree(zip_destination)
    if zipped_filepath.exists():
        os.remove(zipped_filepath)

    return game_set, error_message


def parse_game_files(aoe_game_filenames: List[str], aoe_game_files: list, game_set: GameSet, available_maps: List[str], num_games: int):
    # Check for N attachements based on round
    if len(aoe_game_filenames) < num_games:
        # Send error messages in DM to avoid cluterring channels
        error_message = 'The recently submitted set does not have the correct number of recorded games (attachements). You submitted {} games (attachments) but was expecting {}. If fewer than {} games were played, please submit properly named placeholder games. Discord does not allow editing of attachments so please delete post and resubmit. Thank you'.format(
            len(aoe_game_filenames),
            num_games,
            num_games
        )
        return game_set, error_message

    #Verify games are named properly
    game_map = {}
    for i, file_name in enumerate(aoe_game_filenames):
        is_restore = False

        parsed_names = parse(REC_ALT_3_FRMT, file_name)
        if parsed_names is None: 
            parsed_names = parse(REC_ALT_2_FRMT, file_name)
            if parsed_names is None:
                parsed_names = parse(REC_FRMT, file_name)
                if parsed_names is None:
                    parsed_names = parse(REC_ALT_FRMT, file_name)
            else:
                is_restore = True
        else:
            is_restore = True

        # Verify game numbers are included
        if parsed_names is None:
            error_message = 'The recently submitted set\'s recs are misnamed. Rec names should match this format: {}_vs_{}_G1.aoe2record. Please correct rec names. Thank you'.format(game_set.p1_name, game_set.p2_name)
            return game_set, error_message

        # Convert alphabet to int
        if is_restore: 
            part = parsed_names['part'].lower()[0]
            part = ord(part) - 97
        else:
            part = 0

        # Verify game numbers are included
        if 'game_num' not in parsed_names.named.keys():
            error_message = 'The recently submitted set\'s recs are misnamed. Rec names should match this format: {}_vs_{}_G1.aoe2record. Please correct rec names. Thank you'.format(game_set.p1_name, game_set.p2_name)
            return game_set, error_message

        game_num = int(parsed_names['game_num'])
        game_map[(game_num, part)] = aoe_game_files[i]

    # Get highest part for each game number and sort games by number
    sorted_game_files = {i[0]:game_map[i] for i in sorted(game_map)} 

    # Parse games in order
    num_games_read = 0
    num_games_verified = 0
    for i, aoe_file in sorted_game_files.items():
        # Parse file bytes
        if type(aoe_file) is File:
            match = Summary(aoe_file.fp)
        else:
            with open(aoe_file, 'rb') as aoe_rec:
                match = Summary(aoe_rec)

        # Verify map is in map list
        map_name = match.get_map()['name']
        if map_name not in available_maps:
            error_message = 'The recently submitted set has map mismatch, {} was not in map pool ({}). Please check sample and correct submission. Thank you'.format(map_name, ','.join(available_maps))
            return game_set, error_message
            
        # Get player names and civs
        players = match.get_players()
        ig_player_one_name = players[0]['name']
        ig_player_one_civ = str(players[0]['civilization'])
        ig_player_two_name = players[1]['name']
        ig_player_two_civ = str(players[1]['civilization'])

        # Map civ numbers to names
        _, de_data = get_dataset(Version.DE, None)
        ig_player_one_civ = de_data['civilizations'][ig_player_one_civ]['name']
        ig_player_two_civ = de_data['civilizations'][ig_player_two_civ]['name']

        # Match names
        ig_player_one_name = match_name(ig_player_one_name, game_set.p1_name, game_set.p2_name)
        ig_player_two_name = match_name(ig_player_two_name, game_set.p1_name, game_set.p2_name)

        # Verify civ is in available civs for this player
        if ig_player_one_name == game_set.p1_name:
            # Player one is player one in game, check civs of both players
            if ig_player_one_civ not in game_set.p1_available_civs:
                error_message = 'The recently submitted set has civ mismatch, {} was not in civ pool ({}) for {}. Please check sample and correct submission. Thank you'.format(ig_player_one_civ, ','.join(game_set.p1_available_civs), ig_player_one_name)
                return game_set, error_message
            else:
                player_one_civ = ig_player_one_civ

            if ig_player_two_civ not in game_set.p2_available_civs:
                error_message = 'The recently submitted set has civ mismatch, {} was not in civ pool ({}) for {}. Please check sample and correct submission. Thank you'.format(ig_player_two_civ, ','.join(game_set.p2_available_civs), ig_player_two_name)
                return game_set, error_message
            else:
                player_two_civ = ig_player_two_name
        else:
            # Player one is player one in game, check civs of both players
            if ig_player_one_civ not in game_set.p2_available_civs:
                error_message = 'The recently submitted set has civ mismatch, {} was not in civ pool ({}) for {}. Please check sample and correct submission. Thank you'.format(ig_player_one_civ, ','.join(game_set.p2_available_civs), ig_player_one_name)
                return game_set, error_message
            else:
                player_two_civ = ig_player_one_civ

            if ig_player_two_name not in game_set.p1_available_civs:
                error_message = 'The recently submitted set has civ mismatch, {} was not in civ pool ({}) for {}. Please check sample and correct submission. Thank you'.format(ig_player_two_civ, ','.join(game_set.p1_available_civs), ig_player_two_name)
                return game_set, error_message
            else:
                player_one_civ = ig_player_two_name


        # Record outcome if it was a resign. 
        winning_player = None
        if players[0]['winner'] or players[1]['winner']:
            num_games_verified += 1

            # Identify winner
            if players[0]['winner']:
                winning_player = ig_player_one_name
            else:
                winning_player = ig_player_two_name

        # Record winner
        g = Game()
        g.map = map_name
        g.p1_civ = player_one_civ
        g.p2_civ = player_two_civ
        g.winner = winning_player
        game_set.games.append(g)
                
        # Record number of games read
        num_games_read += 1

        # Check if the series is over
        if game_set.p1_reported_score + game_set.p2_reported_score == num_games_read:
            break

    # Calculate verified scores
    p1_verified_score = 0
    p2_verified_score = 0
    missing_scores = []
    for i_g, g in enumerate(game_set.games):
        if g.winner == game_set.p1_name:
            p1_verified_score += 1
        elif g.winner == game_set.p2_name:
            p2_verified_score += 1
        else:
            missing_scores.append(i_g)

    if len(missing_scores) == 0:
        if game_set.p1_reported_score != p1_verified_score or game_set.p2_reported_score != p2_verified_score:
            error_message = 'The recently submitted set has a score mismatch. You submitted a score of: {}-{} but found recs for a score of {}-{}. Please correct submission. Thank you'.format(
                game_set.p1_reported_score,
                game_set.p2_reported_score,
                p1_verified_score,
                p2_verified_score,
            )
            return game_set, error_message
    else:
        if len(missing_scores) == 1:
            if p1_verified_score < game_set.p1_reported_score:
                game_set.games[missing_scores[0]].winner = game_set.p1_name
            else:
                game_set.games[missing_scores[0]].winner = game_set.p2_name
        else:
            # TODO: How to infer score if more than 1 game ended in defeat
            pass

    return game_set, None
        