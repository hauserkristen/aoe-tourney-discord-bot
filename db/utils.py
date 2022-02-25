class Tournament():
    def __init__(self, name, guild_name):
        self.name = name
        self.guild_name = guild_name

    def to_dict(self):
        return {
            'name': self.name,
            'guild_name': self.guild_name
        }

    def validate(self):
        if self.name is None or self.name == '':
            raise Exception('Tournament name must not be empty but recieved: {}'.format(self.name))
        elif self.guild_name is None or self.guild_name == '':
            raise Exception('Tournament guild name must not be empty but recieved: {}'.format(self.guild_name))
        return True

class Settings():
    def __init__(self):
        pass

    def to_dict(self):
        return {}

    def validate(self):
        return True

class Game():
    def __init__(self):
        self.p1_civ = ''
        self.p2_civ = ''
        self.map = ''
        self.winner = ''

    def to_dict(self, set_id: int, map_id: int, winner_id: int):
        return {
            'set_id': set_id,
            'p1_civ': self.p1_civ,
            'p2_civ': self.p2_civ,
            'map_id': map_id,
            'winner': winner_id
        }

    def validate(self):
        # TODO
        return True

class GameSet():
    def __init__(self):
        self.tourney_name = ''
        self.stage = ''
        self.p1_name = ''
        self.p2_name = ''
        self.games = []

        # Fields not used in DB table
        self.p1_reported_score = 0
        self.p2_reported_score = 0
        self.p1_available_civs = []
        self.p2_available_civs = []
        
    def to_dict(self, tourney_id: int, player_1_id: int, player_2_id: int):
        return {
            'tournament_id': tourney_id,
            'stage': self.stage,
            'p1_id': player_1_id,
            'p2_id': player_2_id
        }

    def validate(self):
        # TODO
        return True

    def to_string(self):
        # For summary channel

        # Record scores
        player_one_score = 0
        player_two_score = 0
        for g in self.games:
            if g.winner == self.p1_name:
                player_one_score += 1
            else:
                player_two_score += 1

        return '{}: {} {} - {} {}'.format(self.stage, self.p1_name, player_one_score, self.p2_name, player_two_score)

class Participant():
    def __init__(self):
        self.tourney_name =  ''
        self.discord_name = ''
        self.in_game_name = ''
        self.aoe2_net_id = 0
        self.reported_current_elo = 0
        self.reported_max_elo = 0
        self.alt_accounts = []
        self.category = ''

    def to_dict(self, tourney_id: int):
        return {
            'tournament_id': tourney_id,
            'name': self.in_game_name,
            'discord_name': self.discord_name,
            'aoe2_net_id': self.aoe2_net_id,
            'current_elo': self.reported_current_elo,
            'max_elo': self.reported_max_elo,
            'alt_accounts': self.alt_accounts,
            'category': self.category
        }

    def validate(self):
        # TODO
        return True