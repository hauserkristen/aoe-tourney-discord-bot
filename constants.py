# Output Channel
SUMMARY_WIDTH = 50

# Map format
MAP_FRMT = 'WW - {map_name}'
VALID_MAPS = [
    'Boundary Brawl',
    'Compass',
    'Golden Hill',
    'Graupel',
    'Houseboat',
    'Inundation',
    'Mired',
    'Nomad'
]

# Strings to round
# TODO: We should move to regex for this probably
STR_TO_STAGE = {
    'Round of 128': 128,
    'Ro128': 128,
    'Round of 64': 64,
    'Ro64': 64,
    'Round of 32': 32,
    'Ro32': 32,
    'Round of 32': 32,
    'Ro32': 32,
    'Round of 16': 16,
    'Ro16': 16,
    'Round of 8': 8,
    'Ro8': 8,
    'QF': 8,
    'Quarters': 8,
    'Quarterfinals': 8,
    'Quarter-finals': 8,
    'Quarter-Finals': 8,
    'Round of 4': 4,
    'Ro4' : 4,
    'SF': 4,
    'Semis': 4,
    'Semifinals': 4,
    'Semi-finals': 4,
    'Semi-Finals': 4,
    'Ro2': 2,
    'Finals': 2
}

# Proper message format
STAGE_FRMT = '[Ss]tage\s*:\s*(.+?)(?:$|\n)'
CIV_DRAFT_FRMT = '[Cc]iv [Dd]raft\s*:\s*(.+?)(?:$|\n)'
SELECTED_MAPS_FRMT = 'HM\s*:\s*(.+?)(?:$|\n)'
PLAYER_ONE_FRMT = '^(.+?)\|'
PLAYER_TWO_FRMT = '[^\|\n]+(?:$|\n)'

# Set up reg expressions for score
SCORE_FRMT = '([^\|\n]+)\|+\s*(\d+)\s*\|+\s*([-:]|vs)\s*\|+\s*(\d+)\s*\|+([^\|\n]+)'
SCORE_ALT_FRMT = '([^\|\n]+)\|+\s*(\d+)\s*([-:]|vs)\s*(\d+)\s*\|+([^\|\n]+)'

# Rec name format
# TODO: Should move to regex
REC_FRMT = '{}_vs_{}_G{game_num}.aoe2record'
REC_ALT_FRMT = '{}_vs_{}-G{game_num}.aoe2record'
REC_ALT_2_FRMT = '{}_vs_{}_G{game_num}{part}.aoe2record'
REC_ALT_3_FRMT = '{}_vs_{}-G{game_num}{part}.aoe2record'

# Registration format
DISCORD_NAME_FRMT =  '[Dd]iscord [Uu]sername\s*:*\s*(.+?)(?:$|\n)'
DISCORD_NAME_ALT_FRMT =  '[Dd]iscord [Nn]ame\s*:*\s*(.+?)(?:$|\n)'
DISCORD_NAME_ALT2_FRMT =  '[Dd]iscord\s*:*\s*(.+?)(?:$|\n)'
IN_GAME_NAME_FRMT =  '[Aa][Oo][Ee]2([\sIiGgDd|]*)[Nn]ame\s*:*\s*(.+?)(?:$|\n)'
IN_GAME_NAME_ALT_FRMT =  '[Aa][Oo][Ee]2([\sIiGgDd|]*)[Uu]sername\s*:*\s*(.+?)(?:$|\n)'
IN_GAME_NAME_ALT2_FRMT =  '[Pp]layer [Nn]ame\s*:*\s*(.+?)(?:$|\n)'
IN_GAME_NAME_ALT3_FRMT =  '[Ii][Gg][Nn]\s*:*\s*(.+?)(?:$|\n)'
PROFILE_LINK_FRMT =  '[Ll]ink to [Aa][Oo][Ee][Nn]exus [Pp]rofile\s*:*\s*(https.+?)(?:$|\n)'
PROFILE_LINK_ALT_FRMT = '[Aa][Oo][Ee]\s*[Nn]exus [Pp]rofile\s*:*\s*(https.+?)(?:$|\n)'
PROFILE_LINK_ALT2_FRMT = '[Aa][Oo][Ee]\s*[Nn]exus\s*:*\s*(https.+?)(?:$|\n)'
PROFILE_LINK_ALT3_FRMT = '[Nn]exus [Pp]rofile\s*:*\s*(https.+?)(?:$|\n)'
PROFILE_LINK_ALT4_FRMT = '[Nn]exus\s*:*\s*(https.+?)(?:$|\n)'
ALT_FRMT = 'Alt accounts\s*:*\s*(.+?)(?:$|\n)'
CURRENT_ELO_FRMT = 'Current [Ee][Ll][Oo]\s*:*\s*(.+?)(?:$|\n)'
MAX_ELO_FRMT = 'Max [Ee][Ll][Oo]\s*:*\s*(.+?)(?:$|\n)'


# Temp directory
TEMP_DIR = 'temp\\parsing_recs'