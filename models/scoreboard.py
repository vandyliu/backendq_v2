import json

from models.stats_endpoint import StatsEndpoint
from models.game import Game

class Scoreboard:
    def __init__(self, date):
        self.date = date
        raw_scoreboard = StatsEndpoint.get_raw_scoreboard(date)
        if not raw_scoreboard:
            raise Exception("Raw scoreboard was not retrieved")
        scoreboard_dict = json.loads(raw_scoreboard)
        # self.scoreboard_dict = scoreboard_dict  # Probably remove to save memory
        self.game_ids = []
        for game in scoreboard_dict["games"]:
            if game["gameId"][0:1] == '0':  # Only NBA Games start with 0
                self.game_ids.append(game["gameId"])
    
    def get_game_ids(self):
        return self.game_ids

    def dictionary(self):
        return self.__dict__

    def get_boxscores(self):
        info = {
            'date': self.date,
            'game_ids': self.game_ids,
            'boxscores': []
        }
        for game_id in self.game_ids:
            boxscore = Game(self.date, game_id).dictionary()
            info['boxscores'].append(boxscore)
        return info
