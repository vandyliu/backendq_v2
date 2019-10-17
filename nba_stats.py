import requests
from requests.exceptions import HTTPError
import json

DATA_NBA_ENDPOINT = "http://data.nba.net/data/10s/prod/v1"


def get_from_data_nba(type, date, game_id=None):
    url = ""
    if type == 'scoreboard':
        url = f"{DATA_NBA_ENDPOINT}/{date}/scoreboard.json"
    elif type == 'boxscore':
        url = f"{DATA_NBA_ENDPOINT}/{date}/{game_id}_boxscore.json"
    elif type == 'mini_boxscore':
        url = f"{DATA_NBA_ENDPOINT}/{date}/{game_id}_mini_boxscore.json"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.content
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


def get_raw_scoreboard(date):
    return get_from_data_nba('scoreboard', date)


def get_raw_boxscore(date, game_id):
    return get_from_data_nba('boxscore', date, game_id)


class Scoreboard:
    def __init__(self, date):
        self.date = date
        raw_scoreboard = get_raw_scoreboard(date)
        if not raw_scoreboard:
            raise Exception("Raw scoreboard was not retrieved")
        scoreboard_dict = json.loads(raw_scoreboard)
        # self.scoreboard_dict = scoreboard_dict  # Probably remove to save memory
        game_ids = []
        for game in scoreboard_dict["games"]:
            if game["gameId"][0:1] == '0':  # Only NBA Games start with 0
                game_ids.append(game["gameId"])


class Game:
    def __init__(self, date, game_id):
        self.date = date
        self.game_id = game_id
        raw_boxscore = get_raw_boxscore(date, game_id)
        if not raw_boxscore:
            raise Exception("Raw boxscore was not retrieved")
        boxscore_dict = json.loads(raw_boxscore)
        # self.boxscore_dict = boxscore_dict  # Probably remove to save memory
        self.is_game_activated = boxscore_dict["basicGameData"]["isGameActivated"]
        self.status_num = boxscore_dict["basicGameData"]["statusNum"]
        self.period = boxscore_dict["basicGameData"]["period"]
        self.v_team = Game.team_score(
            boxscore_dict["basicGameData"]["vTeam"], boxscore_dict["stats"]["vTeam"]
        )
        self.h_team = Game.team_score(
            boxscore_dict["basicGameData"]["hTeam"], boxscore_dict["stats"]["hTeam"]
        )
        for player in boxscore_dict["stats"]["activePlayers"]:
            if player["teamId"] == self.v_team["t_id"]:
                self.v_team["players"].append(player)
            else:
                self.h_team["players"].append(player)
        print(self)
    
    @staticmethod
    def team_score(raw_team_score_info, raw_stats):
        score_info = {
            't_id': raw_team_score_info["teamId"],
            'tri_code': raw_team_score_info["triCode"],
            'win': raw_team_score_info["win"],
            'loss': raw_team_score_info["loss"],
            'score': raw_team_score_info["score"],
            'quarter_scores': [],
            'totals': raw_stats["totals"],
            'leaders': raw_stats["leaders"],
            'players': []
        }
        for i in range(4):
            score_info["quarter_scores"].append(
                raw_team_score_info["linescore"][i]["score"]
            )
        
        return score_info
    

    def dictionary(self):
        return self.__dict__
