#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, render_template
from flask import request,jsonify
from flask import send_from_directory
from flask_cors import CORS, cross_origin
import match

app = Flask(__name__, static_url_path='/static')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app,resource= {
        r"/*":{
        "origins":"*"
    }
}) # This will enable CORS for all routes

matchesJSON = {}
helloJSON = {'resp:hello'}
@app.route('/')
def index():
    matchesJSON = match.getData("Brentford","Fulham")
    return matchesJSON

@app.route('/matches')
def matches():
    print("MATCH_ Request incoming.")
    args = request.args
    home_team = (args.get('homeTeam'))
    away_team = (args.get('awayTeam')) 
    matchesJSON = match.getData(home_team,away_team)
    return matchesJSON

app.run(host='0.0.0.0', port=5050, debug=True)