import json

from models.stats_endpoint import StatsEndpoint
from models.game import Game
from models.exceptions.stats_endpoint_retrieval_exception import StatsEndpointRetrievalException

class Teams:
    def __init__(self, date):
        self.year = date
        raw_teams = StatsEndpoint.get_raw_teams(date)
        if not raw_teams:
            raise StatsEndpointRetrievalException("Raw scoreboard was not retrieved")
        teams_dict = json.loads(raw_teams)