import os
from flask import Flask, jsonify, Response
from dotenv import load_dotenv
import json
from nba_stats import Scoreboard, Game

load_dotenv()

app = Flask(__name__)
app.config.from_object(os.getenv('APP_SETTINGS', None))
print(os.getenv('APP_SETTINGS', None))

@app.route('/')
def boxscores_today():
    return "Hello World!"


@app.route('/date/<date>')
def boxscores(date):
    return "Hello {}!".format(date)


@app.route('/scoreboard/<date>')
def scoreboard(date):
    Scoreboard(date)
    return "Hello {}!".format(date)


@app.route('/date/<date>/<gameid>')
def boxscore(date, gameid):
    g = Game(date, gameid)
    return Response(json.dumps(g.dictionary()), mimetype='application/json')

if __name__ == '__main__':
    app.run()