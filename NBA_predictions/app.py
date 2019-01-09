import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template

from flask_sqlalchemy import SQLAlchemy

import jsons

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
#engine = create_engine('sqlite:///db/schedule_abr.sqlite', connect_args={'check_same_thread': False}, echo=False)

app.config['SQLALCHEMY_DATABASE_URI'] =  False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/schedule_abr.sqlite?check_same_thread=False"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save reference to the tables
Schedule = Base.classes.nba_2018_2019_schedule_logo
TodayPredictions = Base.classes.today_predictions
Stats = Base.classes.stats
YearPredictions = Base.classes.year_predictions

# Create our session (link) from Python to the DB
#session = Session(engine)


#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    """Return the homepage."""
    """Return a list of data for today's games including our predictions for each game"""
    # Query all today games
    results = db.session.query(TodayPredictions).all()

    # Create a dictionary from the row data and append to a list of all_games
    today_games = []
    for t_game in results:
        t_game_dict = {}
        t_game_dict["date"] = t_game.date
        t_game_dict["time"] = t_game.time
        t_game_dict["location"] = t_game.location
        t_game_dict["home_team"] = t_game.home_team
        t_game_dict["road_team"] = t_game.road_team
        t_game_dict["home_team_abr"] = t_game.home_team_abr
        t_game_dict["road_team_abr"] = t_game.road_team_abr
        t_game_dict["road_win_prediction"] = t_game.road_win_prediction
        t_game_dict["home_team_logo"] = t_game.home_team_logo
        t_game_dict["road_team_logo"] = t_game.road_team_logo
        today_games.append(t_game_dict)

    today_json = jsons.dump(today_games)
    print(today_json)
    return render_template("index.html", today_json=today_json)

@app.route("/available_routes")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/schedule<br/>"
        f"/today_predictions<br/>"
        f"/year_predictions<br/>"
        f"/stats"
    )


@app.route("/schedule")
def sched():
    """Return a list of entire schedule"""
    # Query all games on schedule
    results = db.session.query(Schedule).all()

    # Create a dictionary from the row data and append to a list of all_games
    all_games = []
    for game in results:
        game_dict = {}
        game_dict["game_id"] = game.game_id
        game_dict["date"] = game.date
        game_dict["time"] = game.time
        game_dict["location"] = game.location
        game_dict["home_team"] = game.home_team
        game_dict["road_team"] = game.road_team
        game_dict["home_team_abr"] = game.home_team_abr
        game_dict["road_team_abr"] = game.road_team_abr
        game_dict["home_team_logo"] = game.home_team_logo
        game_dict["road_team_logo"] = game.road_team_logo
        all_games.append(game_dict)

    return jsonify(all_games)


@app.route("/today_predictions")
def t_predictions():
    """Return a list of data for today's games including our predictions for each game"""
    # Query all today games
    results = db.session.query(TodayPredictions).all()

    # Create a dictionary from the row data and append to a list of all_games
    today_games = []
    for t_game in results:
        t_game_dict = {}
        t_game_dict["date"] = t_game.date
        t_game_dict["time"] = t_game.time
        t_game_dict["location"] = t_game.location
        t_game_dict["home_team"] = t_game.home_team
        t_game_dict["road_team"] = t_game.road_team
        t_game_dict["home_team_abr"] = t_game.home_team_abr
        t_game_dict["road_team_abr"] = t_game.road_team_abr
        t_game_dict["road_win_prediction"] = t_game.road_win_prediction
        t_game_dict["home_team_logo"] = t_game.home_team_logo
        t_game_dict["road_team_logo"] = t_game.road_team_logo
        today_games.append(t_game_dict)

    return jsonify(today_games)

@app.route("/stats")
def t_stats():
    """Return a list of data for today's games including our predictions for each game"""
    # Query all teams' four factors stats
    results = db.session.query(Stats).all()

    # Create a dictionary from the row data and append to a list of all_games
    today_stats = []
    for t_stat in results:
        t_stat_dict = {}
        t_stat_dict["Team_abbr"] = t_stat.Team_abbr
        t_stat_dict["Offense_eFG"] = t_stat.Offense_eFG
        t_stat_dict["Defense_eFG"] = t_stat.Defense_eFG
        t_stat_dict["Offense_TOV"] = t_stat.Offense_TOV
        t_stat_dict["Defense_TOV"] = t_stat.Defense_TOV
        t_stat_dict["Offense_ORB"] = t_stat.Offense_ORB
        t_stat_dict["Defense_DRB"] = t_stat.Defense_DRB
        t_stat_dict["Offense_FtFga"] = t_stat.Offense_FtFga
        t_stat_dict["Defense_FtFga"] = t_stat.Defense_FtFga
        today_stats.append(t_stat_dict)

    return jsonify(today_stats)

@app.route("/year_predictions")
def y_predictions():
    """Return a list of data for rest of season games including our predictions for each game"""
    # Query all today games
    results = db.session.query(YearPredictions).all()

    # Create a dictionary from the row data and append to a list of all_games
    yr_games = []
    for y_game in results:
        y_game_dict = {}
        y_game_dict["date"] = y_game.date
        y_game_dict["home_team"] = y_game.home_team
        y_game_dict["road_team"] = y_game.road_team
        y_game_dict["home_team_abr"] = y_game.home_team_abr
        y_game_dict["road_team_abr"] = y_game.road_team_abr
        y_game_dict["road_win_prediction"] = y_game.road_win_prediction
        y_game_dict["home_team_logo"] = y_game.home_team_logo
        y_game_dict["road_team_logo"] = y_game.road_team_logo
        yr_games.append(y_game_dict)

    year_json = jsons.dump(yr_games)
    print(year_json)
    return render_template("year_predictions.html", year_json=year_json)

@app.route("/model_accuracy")
def model_accuracy():
    """Return the model_accuracy page."""
    predict_results_url="https://raw.githubusercontent.com/zsubhani/utexas_hw_python/master/model_predictions_results.csv"
    predict_results_df=pd.read_csv(predict_results_url)
    # calculate number of correct predictions, have to convert to normal int
    predict_num_correct = int(predict_results_df['road_win_prediction_correct'].sum())
    # calculate number of total predictions, have to convert to normal int
    predict_count = int(predict_results_df['road_win_prediction_correct'].count())
    # calculate number of incorrect predictions
    predict_num_incorrect = predict_count - predict_num_correct
    # create list of predictions, first value is number correct and second value is number incorrect
    predict_list = [predict_num_correct, predict_num_incorrect]
    return render_template("model_accuracy.html", predict_list=predict_list)


if __name__ == '__main__':
    app.run()