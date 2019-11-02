import json

from models.stats_endpoint import StatsEndpoint
from models.game import Game
from models.exceptions.stats_endpoint_retrieval_exception import StatsEndpointRetrievalException

class Scoreboard:
    def __init__(self, date, file_path=None):
        self.date = date
        scoreboard_dict = {}
        if file_path:
            with open(file_path) as json_file:
                scoreboard_dict = json.load(json_file)
        else:
            raw_scoreboard = StatsEndpoint.get_raw_scoreboard(date)
            if not raw_scoreboard:
                raise StatsEndpointRetrievalException("Raw scoreboard was not retrieved")
            scoreboard_dict = json.loads(raw_scoreboard)
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
            try:
                boxscore = Game(self.date, game_id).dictionary()
                info['boxscores'].append(boxscore)
            except StatsEndpointRetrievalException as e:
                print(f"Stats endpoint retrieval exception: {e}")
            except Exception as err:
                print(f"Generic exception: {err}")
        return info
