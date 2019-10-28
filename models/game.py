import json

from models.stats_endpoint import StatsEndpoint

class Game:
    def __init__(self, date, game_id):
        self.date = date
        self.game_id = game_id
        raw_boxscore = StatsEndpoint.get_raw_boxscore(date, game_id)
        if not raw_boxscore:
            raise Exception("Raw boxscore was not retrieved")
        boxscore_dict = json.loads(raw_boxscore)
        # self.boxscore_dict = boxscore_dict  # Remove to save memory
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
        
        if "playoffs" in boxscore_dict["basicGameData"]:
            self.game_text = boxscore_dict["basicGameData"]["playoffs"]["seriesSummaryText"]
    

    @staticmethod
    def team_score(raw_team_score_info, raw_stats):
        score_info = {
            't_id': raw_team_score_info["teamId"],
            'name': Game.get_full_team_name(raw_team_score_info["triCode"]),
            'tri_code': raw_team_score_info["triCode"],
            'win': raw_team_score_info["win"],
            'loss': raw_team_score_info["loss"],
            'score': raw_team_score_info["score"],
            'quarter_scores': [],
            'totals': raw_stats["totals"],
            'leaders': raw_stats["leaders"],
            'players': []
        }
        for i in range(len(raw_team_score_info["linescore"])):
            score_info["quarter_scores"].append(
                raw_team_score_info["linescore"][i]["score"]
            )
        
        return score_info
    
    @staticmethod
    def get_full_team_name(tri_code):
        team = ""
        if tri_code == "ATL":
            team = "Atlanta Hawks"
        elif tri_code == "BKN":
            team = "Brooklyn Nets"
        elif tri_code == "BOS":
            team = "Boston Celtics"
        elif tri_code == "CHA":
            team = "Charlotte Hornets"
        elif tri_code == "CHI":
            team = "Chicago Bulls"
        elif tri_code == "CLE":
            team = "Cleveland Cavaliers"
        elif tri_code == "DAL":
            team = "Dallas Mavericks"
        elif tri_code == "DEN":
            team = "Denver Nuggets"
        elif tri_code == "DET":
            team = "Detroit Pistons"
        elif tri_code == "GSW":
            team = "Golden State Warriors"
        elif tri_code == "HOU":
            team = "Houston Rockets"
        elif tri_code == "IND":
            team = "Indiana Pacers"
        elif tri_code == "LAC":
            team = "Los Angeles Clippers"
        elif tri_code == "LAL":
            team = "Los Angeles Lakers"
        elif tri_code == "MEM":
            team = "Memphis Grizzlies"
        elif tri_code == "MIA":
            team = "Miami Heat"
        elif tri_code == "MIL":
            team = "Milwaukee Bucks"
        elif tri_code == "MIN":
            team = "Minnesota Timberwolves"
        elif tri_code == "NOP":
            team = "New Orleans Pelicans"
        elif tri_code == "NYK":
            team = "New York Knicks"
        elif tri_code == "OKC":
            team = "Oklahoma City Thunder"
        elif tri_code == "ORL":
            team = "Orlando Magic"
        elif tri_code == "PHI":
            team = "Philadelphia 76ers"
        elif tri_code == "PHX":
            team = "Phoenix Suns"
        elif tri_code == "POR":
            team = "Portland Trail Blazers"
        elif tri_code == "SAC":
            team = "Sacramento Kings"
        elif tri_code == "SAS":
            team = "San Antonio Spurs"
        elif tri_code == "TOR":
            team = "Toronto Raptors"
        elif tri_code == "UTA":
            team = "Utah Jazz"
        elif tri_code == "WAS":
            team = "Washington Wizards"
        return team

    def dictionary(self):
        return self.__dict__