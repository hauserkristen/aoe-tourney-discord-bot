# External Imports
from requests import get

def query_elo(profile_id: int):
    # Query aoe2.net
    QUERY_STRING = 'https://aoe2.net/api/player/ratinghistory?game=aoe2de&leaderboard_id=3&profile_id={}&count=10000'.format(profile_id)
    retries = 0
    success = False
    while not success and retries < 10:
        try:
            response = get(QUERY_STRING)
            success = True
        except (ConnectionError, TimeoutError):
            retries += 1
            successful_retrieval = False
    
    # Check for success
    successful_retrieval = response.status_code == 200

    # Get data
    if successful_retrieval:
        profile_info = response.json()

    # Calculate current and max
    current_elo = profile_info[0]['rating']
    max_elo = max([g['rating'] for g in profile_info])

    return current_elo, max_elo