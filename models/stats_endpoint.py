import json

import requests
from requests.exceptions import HTTPError

DATA_NBA_ENDPOINT = "http://data.nba.net/data/10s/prod/v1"

class StatsEndpoint:
    @staticmethod
    def get_from_data_nba(type, date, game_id=None):
        url = ""
        if type == 'scoreboard':
            url = f"{DATA_NBA_ENDPOINT}/{date}/scoreboard.json"
        elif type == 'boxscore':
            url = f"{DATA_NBA_ENDPOINT}/{date}/{game_id}_boxscore.json"
        elif type == 'mini_boxscore':
            url = f"{DATA_NBA_ENDPOINT}/{date}/{game_id}_mini_boxscore.json"
        elif type == 'teams':
            # date is actually just a year
            url = f"{DATA_NBA_ENDPOINT}/{date}/teams.json"
        try:
            print(f'Accessing: {url}')
            resp = requests.get(url)
            resp.raise_for_status()
            return resp.content
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')

    @staticmethod
    def get_raw_scoreboard(date):
        return StatsEndpoint.get_from_data_nba('scoreboard', date)

    @staticmethod
    def get_raw_boxscore(date, game_id):
        return StatsEndpoint.get_from_data_nba('boxscore', date, game_id)

    @staticmethod
    def get_raw_teams(date):
        return StatsEndpoint.get_from_data_nba('teams', date)
