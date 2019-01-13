# Python script to generate NBA game predictions for 2018-2019 season
########################################################################## 

# Dependencies
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
import os
import bs4
import splinter
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import re
import time
import datetime
from datetime import date
import sqlalchemy
from sqlalchemy import create_engine

# -------------------------------------------------------------------
# Step 1 Machine Learning Model using SVM linear classifier
# -------------------------------------------------------------------

# Read in dataset that has regular season game data from 2012-2018
df = pd.read_csv("db/2012-18_teamBoxScore_diff_columns.csv")
df.head()

df.shape

# drop any rows with NaN values
df = df.dropna(how='any') 

df.shape

target = df["outcome"]
target_names = ["loss", "win"]

# only focus on the columns for the four factors (four offense and four defense so technically 8 total)
# put that into new dataframe
df1 = df[['diff_teamEFG%','diff_opptEFG%', 'diff_teamTO%', 'diff_opptTO%', 'diff_OREB%', 'diff_DREB%', 'diff_teamFTF', 'diff_opptFTF', 'outcome']]
df1.head()

# new dataframe with 'outcome' dropped
data = df1.drop("outcome", axis=1)
feature_names = data.columns
data.head()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(data, target, random_state=42)

# Support vector machine linear classifier
from sklearn.svm import SVC 
model = SVC(kernel='linear')
model.fit(X_train, y_train)

# Model Accuracy
print('Test Acc: %.3f' % model.score(X_test, y_test))

# Calculate classification report
from sklearn.metrics import classification_report
predictions = model.predict(X_test)
print(classification_report(y_test, predictions,
                            target_names=target_names))

# create function to make predictions
#
# returns string 'Win' if road team is predicted to win
# returns string 'Loss' if road team is predicted to lose
def predict_outcome_win_loss(road_team_abbr, road_team_stats, home_team_stats):
    road_team_array = np.array(road_team_stats)
    home_team_array = np.array(home_team_stats)
    diffs = road_team_array - home_team_array
    diffs_l = [diffs]
    prediction = model.predict(diffs_l)
    print(prediction)
    if ((prediction==1.).all()==True):
        print('Prediction is a Win for ' + str(road_team_abbr))
        outcome = 'Win'
    else:
        print('Prediction is a Loss for ' + str(road_team_abbr))
        outcome = 'Loss'
    return outcome

#Testing out prediction manually for sanity check purposes

# Game DEN at SAC
den_stats = [.524, .513, 12.1, 12.2, 27.5, 77.7, .186, .191]
sac_stats = [.531, .536, 11.6, 13.7, 22.0, 74.8, .173, .209]
result = predict_outcome_win_loss('DEN', den_stats, sac_stats)
print(result)

# --------------------------------------------------------------------------------
# Step 2 Web scraping to capture updated daily stats from basketball-reference.com
# --------------------------------------------------------------------------------

#teams list
teams = ['ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'DET',
         'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN',
         'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS',
         'TOR', 'UTA', 'WAS']

# load web pages without loading images in selenium
from selenium import webdriver

chromeOptions = webdriver.ChromeOptions()
prefs = {'profile.managed_default_content_settings.images':2, 'disk-cache-size': 4096}
chromeOptions.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chromeOptions)

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False, options=chromeOptions)

# visit main page first
main_url = 'https://www.basketball-reference.com/'
browser.visit(main_url)
# wait before going through loop of each team's stats
time.sleep(60)

# loop to start the scraping of the stats
team_list = []
x = 0 
while x == 0:
    try:
        for team in teams:
            # URL
            url = r"https://www.basketball-reference.com/teams/" + team + "/2019.html"
            browser.visit(url)

            # add some delay
            time.sleep(20)

            stat_list = []

            #Path to get titles of articles
            team_X = team
            oEfg_X = '//*[@id="team_misc"]/tbody/tr[1]/td[13]'
            dEfg_X = '//*[@id="team_misc"]/tbody/tr[1]/td[17]'
            oTOV_X = '//*[@id="team_misc"]/tbody/tr[1]/td[14]'
            dTOV_X = '//*[@id="team_misc"]/tbody/tr[1]/td[18]'
            oORB_X = '//*[@id="team_misc"]/tbody/tr[1]/td[15]'
            dDRB_X = '//*[@id="team_misc"]/tbody/tr[1]/td[19]'
            oFtByFga_X = '//*[@id="team_misc"]/tbody/tr[1]/td[16]'
            dFtByFga_X = '//*[@id="team_misc"]/tbody/tr[1]/td[20]'

            #Reading the results  
            abr = team_X
            stat_list.append(abr)
            oEfg = browser.find_by_xpath(oEfg_X).value
            stat_list.append(oEfg)
            dEfg = browser.find_by_xpath(dEfg_X).value
            stat_list.append(dEfg)
            oTOV = browser.find_by_xpath(oTOV_X).value
            stat_list.append(oTOV)
            dTOV = browser.find_by_xpath(dTOV_X).value
            stat_list.append(dTOV)
            oORB = browser.find_by_xpath(oORB_X).value
            stat_list.append(oORB)
            dDRB = browser.find_by_xpath(dDRB_X).value
            stat_list.append(dDRB)
            oFtByFga = browser.find_by_xpath(oFtByFga_X).value
            stat_list.append(oFtByFga)
            dFtByFga = browser.find_by_xpath(dFtByFga_X).value
            stat_list.append(dFtByFga)

            team_list.append(stat_list)
            print(team_list)
        x = 1
    except:
        print("try again")

# Create a dataframe that has updated stats for all of the teams
stats_df = pd.DataFrame(team_list)
stats_df.columns = ['Team_abbr','Offense_eFG','Defense_eFG','Offense_TOV','Defense_TOV','Offense_ORB','Defense_DRB','Offense_FtFga','Defense_FtFga']
stats_df

# -------------------------------------------------------------------------------------
# Step 3 Update database (sqlite file) with 8 factors for each team (in 'stats') table
# -------------------------------------------------------------------------------------

# setup database connection
stats_engine = create_engine('sqlite:///db/schedule_abr.sqlite')
# send stats dataframe to stats table in database file
stats_df.to_sql('stats', stats_engine, if_exists='replace', index=False)

# test that we can query from stats table in db
stats_sql_df = pd.read_sql_query('SELECT * FROM stats',stats_engine)
stats_sql_df.head()

# NEED TO SET PRIMARY KEY after to_sql is done so that later sqlalchemy can interact with the stats table

import sqlite3
#connect to the database
conn = sqlite3.connect('db/schedule_abr.sqlite')
c = conn.cursor()

c.executescript('''
    PRAGMA foreign_keys=off;
    BEGIN TRANSACTION;
    ALTER TABLE stats RENAME TO old_stats;
    /*create a new table with the same column names and types while
    defining a primary key for the desired column*/
    CREATE TABLE stats (Team_abbr text NOT NULL PRIMARY KEY,
                            Offense_eFG REAL NOT NULL,
                            Defense_eFG REAL NOT NULL,
                            Offense_TOV REAL NOT NULL,
                            Defense_TOV REAL NOT NULL,
                            Offense_ORB REAL NOT NULL,
                            Defense_DRB REAL NOT NULL,
                            Offense_FtFga REAL NOT NULL,
                            Defense_FtFga REAL NULL);
    INSERT INTO stats SELECT * FROM old_stats;
    DROP TABLE old_stats;
    COMMIT TRANSACTION;
    PRAGMA foreign_keys=on;''')

#close out the connection
c.close()
conn.close()

# -------------------------------------------------------------------------------------
# Step 4 Find out each game that is being played today from database (in 'nba_2018_2019_schedule_logo' table)
# -------------------------------------------------------------------------------------

# setup database connection
schedule_engine = create_engine('sqlite:///db/schedule_abr.sqlite')
# test that we can query from nba_2018_2019_schedule_logo table in database file
schedule_sql_df = pd.read_sql_query('SELECT * FROM nba_2018_2019_schedule_logo',schedule_engine)
schedule_sql_df.head()

# function to get today's date in same format as 'date' column of nba_2018_2019_schedule_logo table in database
# format is mm/dd/yyyy example: 1/6/2019

def get_todays_date():
    today = str(date.today())
    todays_date = date.today().strftime('%m/%d/%Y')
    print(todays_date)
    todays_date_month_first_two = todays_date[0:2]
    print(todays_date_month_first_two)
    newstr = todays_date_month_first_two
    if todays_date_month_first_two[0] == '0':
        newstr = todays_date_month_first_two.replace("0", "")
    print(newstr)
    todays_date_day_first_two = todays_date[3:5]
    print(todays_date_day_first_two)
    newstr2 = todays_date_day_first_two
    if todays_date_day_first_two[0] == '0':
        newstr2 = todays_date_day_first_two.replace("0", "")
    print(newstr2)
    newstr3 = todays_date[5:]
    final_date_string = newstr + '/' + newstr2 + newstr3
    return final_date_string

# test out function to get today's date
schedule_date = get_todays_date()
schedule_date

# function to get only today's games from schedule table into a dataframe
# this queries database

def get_todays_games(sch_date):
    cmd1 = 'SELECT * FROM nba_2018_2019_schedule_logo WHERE date='
    print(cmd1)
    cmd2 = "'"
    print(cmd2)
    cmd3 = "'"
    print(cmd3)
    cmd = cmd1 + cmd2 + schedule_date + cmd3
    print(cmd)
    schedule_today_df = pd.read_sql_query(cmd,schedule_engine)
    return schedule_today_df

# get only today's games into a dataframe
todays_games_df = get_todays_games(schedule_date)
todays_games_df

# -------------------------------------------------------------------------------------
# Step 5
# a) get updated stats into arrays for road and home teams for each game being played today
# b) make prediction for road team for each game being played today
# -------------------------------------------------------------------------------------

# function to get updated stats for an individual team using stats dataframe

def capture_updated_stats(team_name, df):
    team_row = df.loc[df['Team_abbr'] == team_name]
    print('Capturing stats for ' + team_name)
    team_O_EFG = float(team_row.iloc[0][1])
    team_D_EFG = float(team_row.iloc[0][2])
    team_O_TOV = float(team_row.iloc[0][3])
    team_D_TOV = float(team_row.iloc[0][4])
    team_O_ORB = float(team_row.iloc[0][5])
    team_D_DRB = float(team_row.iloc[0][6])
    team_O_FTF = float(team_row.iloc[0][7])
    team_D_FTF = float(team_row.iloc[0][8])
    print('values after iloc and converting to float are...')
    print(team_O_EFG)
    print(team_D_EFG)
    print(team_O_TOV)
    print(team_D_TOV)
    print(team_O_ORB)
    print(team_D_DRB)
    print(team_O_FTF)
    print(team_D_FTF)
    team_stats_array = [team_O_EFG, team_D_EFG, team_O_TOV, team_D_TOV, team_O_ORB, team_D_DRB, team_O_FTF, team_D_FTF]
    return team_stats_array

# function to iterate through all rows of schedule dataframe
# capture stats for road team and home team
# prediction for road team is made ('Win' or 'Loss') and dataframe is modified

def prediction_iterrow(sch_df, sta_df):
    for (i, row) in sch_df.iterrows():
        home_team_abr_val = row['home_team_abr']
        road_team_abr_val = row['road_team_abr']
        road_win_prediction_val = row['road_win_prediction']
        print(home_team_abr_val, road_team_abr_val, road_win_prediction_val)
        road_team_stats = capture_updated_stats(road_team_abr_val,sta_df)
        print('Road team stats--------->')
        print(road_team_stats)
        home_team_stats = capture_updated_stats(home_team_abr_val,sta_df)
        print('Home team stats--------->')
        print(home_team_stats)
        our_prediction = predict_outcome_win_loss(road_team_abr_val, road_team_stats, home_team_stats)
        print(our_prediction)
        print('Our Prediction for ' + road_team_abr_val + ' vs. ' + home_team_abr_val + ' is: ' + our_prediction)
        sch_df.at[i,'road_win_prediction'] = our_prediction

# create a today's stats dataframe equal to stats_sql_df we had gotten from scraping earlier
todays_stats_df = stats_sql_df
todays_stats_df.head()

# show today's games dataframe again
todays_games_df.head()

# run function that will use todays_stats_df to modify road_win_prediction column in todays_games_df
prediction_iterrow(todays_games_df, todays_stats_df)

# now road_win_prediction column in todays_games_df should be updated with our predictions
todays_games_df

# update SQL database in a table called 'today_predictions' with our predictions for today's games
schedule_abr_engine = create_engine('sqlite:///db/schedule_abr.sqlite')
todays_games_df.to_sql('today_predictions', schedule_abr_engine, if_exists='replace', index=False)

# test that we can query from today_predictions table in db
today_predictions_sql_df = pd.read_sql_query('SELECT * FROM today_predictions',schedule_abr_engine)
today_predictions_sql_df.head()

# NEED TO SET PRIMARY KEY after to_sql is done so that later sqlalchemy can interact with the today_predictions table

import sqlite3
#connect to the database
conn = sqlite3.connect('db/schedule_abr.sqlite')
c = conn.cursor()

c.executescript('''
    PRAGMA foreign_keys=off;
    BEGIN TRANSACTION;
    ALTER TABLE today_predictions RENAME TO old_table;
    /*create a new table with the same column names and types while
    defining a primary key for the desired column*/
    CREATE TABLE today_predictions (game_id INTEGER NOT NULL PRIMARY KEY,
                            date text NOT NULL,
                            time text NOT NULL,
                            location text NOT NULL,
                            home_team text NOT NULL,
                            road_team text NOT NULL,
                            home_score INTEGER NOT NULL,
                            road_score INTEGER NOT NULL,
                            result text NOT NULL,
                            home_team_abr text NOT NULL,
                            road_team_abr text NOT NULL,
                            road_win_prediction text NOT NULL,
                            home_team_logo text NOT NULL,
                            road_team_logo text NOT NULL);
    INSERT INTO today_predictions SELECT * FROM old_table;
    DROP TABLE old_table;
    COMMIT TRANSACTION;
    PRAGMA foreign_keys=on;''')

#close out the connection
c.close()
conn.close()

# -------------------------------------------------------------------------------------
# Step 6
# a) get updated stats into arrays for road and home teams for each game being played in 2019 (rest of season)
# b) make prediction for road team for each game being played in 2019 (rest of season)
# -------------------------------------------------------------------------------------
# create a current stats dataframe equal to stats_sql_df we had gotten from scraping earlier
current_stats_df = stats_sql_df
current_stats_df.head()

# function to get a year's games from schedule table into a dataframe
# this queries database

def get_year_games(year):
    cmd1 = 'SELECT game_id, date, home_team, road_team, home_team_abr, road_team_abr, road_win_prediction, home_team_logo, road_team_logo FROM nba_2018_2019_schedule_logo WHERE substr(date, 5, 4)='
    print(cmd1)
    cmd2 = "'"
    print(cmd2)
    cmd3 = "'"
    print(cmd3)
    cmd4 = 'or substr(date, 6, 4)='
    print(cmd4)
    cmd5 = "'"
    print(cmd2)
    cmd6 = "'"
    print(cmd3)
    cmd = cmd1 + cmd2 + year + cmd3 + cmd4 + cmd5 + year + cmd6
    print(cmd)
    schedule_year_df = pd.read_sql_query(cmd,schedule_engine)
    return schedule_year_df

# get 2019's games into a dataframe
season_year = '2019'
year_games_df = get_year_games(season_year)
year_games_df.head()

# run function that will use current_stats_df to modify road_win_prediction column in year_games_df
prediction_iterrow(year_games_df, current_stats_df)

# update SQL database in a table called 'year_predictions' with our predictions for the rest of season (year) games
year_schedule_abr_engine = create_engine('sqlite:///db/schedule_abr.sqlite')
year_games_df.to_sql('year_predictions', year_schedule_abr_engine, if_exists='replace', chunksize=75, index=False)

# test that we can query from year_predictions table in db
year_predictions_sql_df = pd.read_sql_query('SELECT * FROM year_predictions',schedule_abr_engine)
year_predictions_sql_df.head()

# NEED TO SET PRIMARY KEY after to_sql is done so that later sqlalchemy can interact with the today_predictions table

import sqlite3
#connect to the database
conn = sqlite3.connect('db/schedule_abr.sqlite')
c = conn.cursor()

c.executescript('''
    PRAGMA foreign_keys=off;
    BEGIN TRANSACTION;
    ALTER TABLE year_predictions RENAME TO old_year_table;
    /*create a new table with the same column names and types while
    defining a primary key for the desired column*/
    CREATE TABLE year_predictions (game_id INTEGER NOT NULL PRIMARY KEY,
                            date text NOT NULL,
                            home_team text NOT NULL,
                            road_team text NOT NULL,
                            home_team_abr text NOT NULL,
                            road_team_abr text NOT NULL,
                            road_win_prediction text NOT NULL,
                            home_team_logo text NOT NULL,
                            road_team_logo text NOT NULL);
    INSERT INTO year_predictions SELECT * FROM old_year_table;
    DROP TABLE old_year_table;
    COMMIT TRANSACTION;
    PRAGMA foreign_keys=on;''')

#close out the connection
c.close()
conn.close()

#------------------------------------------------------------------
print('End of game_predictions.py script')
# That is all for now. 