import json
import os

from dotenv import load_dotenv
from flask import Flask, Response, jsonify

from models.game import Game
from models.scoreboard import Scoreboard
from models.stats_endpoint import StatsEndpoint

load_dotenv()

app = Flask(__name__)
app.config.from_object(os.getenv('APP_SETTINGS', None))
print(os.getenv('APP_SETTINGS', None))

@app.route('/')
def boxscores_today():
    return "Hello World!"

@app.route('/date/<date>')
def boxscores(date):
    try:
        s = Scoreboard(date)
        return Response(json.dumps(s.get_boxscores()), mimetype='application/json')
    except:
        no_info = {
            'game_ids': [],
            'amount_of_games': 0,
            'boxscores': []
        }
        return Response(json.dumps(no_info), mimetype='application/json')


@app.route('/date/<date>/<gameid>')
def boxscore(date, gameid):
    g = Game(date, gameid)
    return Response(json.dumps(g.dictionary()), mimetype='application/json')


@app.route('/games/<date>')
def games(date):
    s = Scoreboard(date)
    return Response(json.dumps(s.dictionary()), mimetype='application/json')


@app.route('/mock/date/')
def hardcode_boxscores():
    s = Scoreboard("20191102", "examples/raw_scoreboard_no_games_ready.json")
    return Response(json.dumps(s.get_boxscores()), mimetype='application/json')

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = r'http://localhost:3000'
    return response

if __name__ == '__main__':
    app.run()
