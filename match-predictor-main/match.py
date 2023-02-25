import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import requests
import re
import time
import json



#Load data from top 5 leagues (CL Knockout Games and League Matches)
df_ESP = pd.read_csv('SP1.csv',index_col=False) #SPAIN LA LIGA
df_FR = pd.read_csv('F1.csv',index_col=False) #FRANCE LIGUE 1
df_ENG = pd.read_csv('E0.csv',index_col=False) #ENGLAND PREMIER LEAGUE
df_GER = pd.read_csv('D1.csv',index_col=False) #GERMANY BUNDESLIGA
df_ITA = pd.read_csv('I1.csv',index_col=False) #ITALY SERIE A

#Load data from other leagues (Mainly for Europa League matches and CL Group Stage matches)

df_B = pd.read_csv('B1.csv',index_col=False) #BELGIAN JUPILER LEAGUE
df_N = pd.read_csv('N1.csv',index_col=False) #NETHERLANDS EREDIVISIE
df_P = pd.read_csv('P1.csv',index_col=False) #PORTUGESE LEAGUE
df_T = pd.read_csv('T1.csv',index_col=False) #TURKISH LEAGUE
df_G = pd.read_csv('G1.csv',index_col=False) #GREECE LEAGUE
df_POL = pd.read_csv('POL.csv',index_col=False) #POLISH LEAGUE
df_NOR = pd.read_csv('NOR.csv',index_col=False) #NORWEGIAN LEAGUE

#Transforming Polish and Norwegian Leagues into required format
df_POL.columns=['Country','League','Season','Date','Time','HomeTeam','AwayTeam','FTHG','FTAG','Res','PH','PD','PA','MaxH','MaxD','MaxA','AvgH','AvgD','AvgA']
df_NOR.columns=['Country','League','Season','Date','Time','HomeTeam','AwayTeam','FTHG','FTAG','Res','PH','PD','PA','MaxH','MaxD','MaxA','AvgH','AvgD','AvgA']

#Because it is NOT yet a database accessed system, everything is stored in variables.

#Primary leagues
df_ESPFR = pd.concat([df_ESP,df_FR],axis=0) #Concatenating dataframes.
df_ESPFRENG =  pd.concat([df_ESPFR,df_ENG],axis=0) #Concatenating dataframes.
df_ESPFRENGGER =  pd.concat([df_ESPFRENG,df_GER],axis=0) #Concatenating dataframes.
df_ESPFRENGGERITA =  pd.concat([df_ESPFRENGGER,df_ITA],axis=0) #Concatenating dataframes.

#Secondary leagues
df_BN = pd.concat([df_B,df_N],axis=0) #Concatenating dataframes.
df_BNP = pd.concat([df_BN,df_P],axis=0) #Concatenating dataframes.
df_BNPT = pd.concat([df_BNP,df_T],axis=0) #Concatenating dataframes.
df_BNPTG = pd.concat([df_BNP,df_G],axis=0) #Concatenating dataframes.
df_NORPOL = pd.concat([df_NOR,df_POL],axis=0) #Concatenating dataframes.

#Final dataframe
df_semi = pd.concat([df_ESPFRENGGERITA,df_BNPTG],axis=0) #Concatenating dataframes.
df = pd.concat([df_semi,df_NORPOL]) #Adding Poland and Norway.

df.reset_index(drop=True, inplace=True)

def calculate(home_,away_):
    #Team names
    #home_team_name = input() #User input from console for home team.
    home_team_name = home_  #YOU CAN ADD NAME BY PLAIN STRING
    #away_team_name = input() #User input from console for away team.
    away_team_name = away_  #YOU CAN ADD NAME BY PLAIN STRING

    #Collect data for Home Team
    #-------------------------------
    HomeTeamHomeGames = df.loc[df['HomeTeam'] == home_team_name]
    HomeTeamAwayGames = df.loc[df['AwayTeam'] == home_team_name]

    HomeTeamHomeGamesOnly = df.loc[df['HomeTeam'] == home_team_name]['AwayTeam']
    HomeTeamAwayGamesOnly = df.loc[df['AwayTeam'] == home_team_name]['HomeTeam']

    HomeTeamHomeGoals = df.loc[df['HomeTeam'] == home_team_name]['FTHG']
    HomeTeamAwayGoals = df.loc[df['AwayTeam'] == home_team_name]['FTAG']

    HomeTeamHomeConceded = df.loc[df['HomeTeam'] == home_team_name]['FTAG']
    HomeTeamAwayConceded = df.loc[df['AwayTeam'] == home_team_name]['FTHG']

    HomeTeamHomeShots = HomeTeamHomeGames.loc[df['HomeTeam'] == home_team_name]['HS']
    HomeTeamAwayShots = HomeTeamAwayGames.loc[df['AwayTeam'] == home_team_name]['AS']

    HomeTeamHomeShotsAgainst = HomeTeamHomeGames.loc[df['HomeTeam'] == home_team_name]['AS']
    HomeTeamAwayShotsAgainst = HomeTeamAwayGames.loc[df['AwayTeam'] == home_team_name]['HS']

    HomeTeamHomeShotsTarget = HomeTeamHomeGames.loc[df['HomeTeam'] == home_team_name]['HST']
    HomeTeamAwayShotsTarget = HomeTeamAwayGames.loc[df['AwayTeam'] == home_team_name]['AST']

    HomeTeamHomeShotsTargetAgainst = HomeTeamHomeGames.loc[df['HomeTeam'] == home_team_name]['AST']
    HomeTeamAwayShotsTargetAgainst = HomeTeamAwayGames.loc[df['AwayTeam'] == home_team_name]['HST']

    HomeTeamHomeCorners = HomeTeamHomeGames.loc[df['HomeTeam'] == home_team_name]['HC']
    HomeTeamAwayCorners = HomeTeamAwayGames.loc[df['AwayTeam'] == home_team_name]['AC']

    HomeTeamHomeYellows = HomeTeamHomeGames.loc[df['HomeTeam'] == home_team_name]['HY']
    HomeTeamAwayYellows = HomeTeamAwayGames.loc[df['AwayTeam'] == home_team_name]['AY']

    HomeTeamHomeReds = HomeTeamHomeGames.loc[df['HomeTeam'] == home_team_name]['HR']
    HomeTeamAwayReds = HomeTeamAwayGames.loc[df['AwayTeam'] == home_team_name]['AR']

    HomeTeamHomeFouls = HomeTeamHomeGames.loc[df['HomeTeam'] == home_team_name]['HF']
    HomeTeamAwayFouls = HomeTeamAwayGames.loc[df['AwayTeam'] == home_team_name]['AF']

    #--------------------------------


    #Collect data for Away Team
    #--------------------------------

    AwayTeamHomeGames = df.loc[df['HomeTeam'] == away_team_name]
    AwayTeamAwayGames = df.loc[df['AwayTeam'] == away_team_name]

    AwayTeamHomeGamesOnly = df.loc[df['HomeTeam'] == away_team_name]['AwayTeam']
    AwayTeamAwayGamesOnly = df.loc[df['AwayTeam'] == away_team_name]['HomeTeam']

    AwayTeamHomeGoals = df.loc[df['HomeTeam'] == away_team_name]['FTHG']
    AwayTeamAwayGoals = df.loc[df['AwayTeam'] == away_team_name]['FTAG']

    AwayTeamHomeConceded = df.loc[df['HomeTeam'] == away_team_name]['FTAG']
    AwayTeamAwayConceded = df.loc[df['AwayTeam'] == away_team_name]['FTHG']

    AwayTeamHomeShots = AwayTeamHomeGames.loc[df['HomeTeam'] == away_team_name]['HS']
    AwayTeamAwayShots = AwayTeamAwayGames.loc[df['AwayTeam'] == away_team_name]['AS']

    AwayTeamHomeShotsTarget = AwayTeamHomeGames.loc[df['HomeTeam'] == away_team_name]['HST']
    AwayTeamAwayShotsTarget = AwayTeamAwayGames.loc[df['AwayTeam'] == away_team_name]['AST']

    AwayTeamHomeShots = AwayTeamHomeGames.loc[df['HomeTeam'] == away_team_name]['HS']
    AwayTeamAwayShots = AwayTeamAwayGames.loc[df['AwayTeam'] == away_team_name]['AS']

    AwayTeamHomeShotsAgainst = AwayTeamHomeGames.loc[df['HomeTeam'] == away_team_name]['AS']
    AwayTeamAwayShotsAgainst = AwayTeamAwayGames.loc[df['AwayTeam'] == away_team_name]['HS']

    AwayTeamHomeShotsTarget = AwayTeamHomeGames.loc[df['HomeTeam'] == away_team_name]['HST']
    AwayTeamAwayShotsTarget = AwayTeamAwayGames.loc[df['AwayTeam'] == away_team_name]['AST']

    AwayTeamHomeShotsTargetAgainst = AwayTeamHomeGames.loc[df['HomeTeam'] == away_team_name]['AST']
    AwayTeamAwayShotsTargetAgainst = AwayTeamAwayGames.loc[df['AwayTeam'] == away_team_name]['HST']

    AwayTeamHomeCorners = AwayTeamHomeGames.loc[df['HomeTeam'] == away_team_name]['HC']
    AwayTeamAwayCorners = AwayTeamAwayGames.loc[df['AwayTeam'] == away_team_name]['AC']

    AwayTeamHomeYellows = AwayTeamHomeGames.loc[df['HomeTeam'] == away_team_name]['HY']
    AwayTeamAwayYellows = AwayTeamAwayGames.loc[df['AwayTeam'] == away_team_name]['AY']

    AwayTeamHomeReds = AwayTeamHomeGames.loc[df['HomeTeam'] == away_team_name]['HR']
    AwayTeamAwayReds = AwayTeamAwayGames.loc[df['AwayTeam'] == away_team_name]['AR']

    AwayTeamHomeFouls = AwayTeamHomeGames.loc[df['HomeTeam'] == away_team_name]['HF']
    AwayTeamAwayFouls = AwayTeamAwayGames.loc[df['AwayTeam'] == away_team_name]['AF']

    #--------------------------------

    #Create data from them
    #--------------------------------

    home_avg_goals = HomeTeamHomeGoals.mean()
    home_avg_goals_away = HomeTeamAwayGoals.mean()

    home_avg_shots = HomeTeamHomeShots.mean()
    home_avg_shots_away = HomeTeamAwayShots.mean()

    home_avg_ontarget = HomeTeamHomeShotsTarget.mean()
    home_avg_ontarget_away = HomeTeamAwayShotsTarget.mean()

    home_avg_ontarget_against = HomeTeamHomeShotsTargetAgainst.mean()

    home_shot_pg = HomeTeamHomeShots.mean() / HomeTeamHomeGoals.mean()
    home_shot_pg_away = HomeTeamAwayShots.mean() / HomeTeamAwayGoals.mean()

    home_avg_yellow = HomeTeamHomeYellows.mean()
    home_avg_yellow_away = HomeTeamAwayYellows.mean()

    home_avg_reds = HomeTeamHomeReds.mean()
    home_avg_reds_away = HomeTeamAwayReds.mean()

    home_avg_fouls_home = HomeTeamHomeFouls.mean()
    home_avg_fouls_away = HomeTeamAwayFouls.mean()

    away_avg_goals = AwayTeamAwayGoals.mean()
    away_avg_goals_home = AwayTeamHomeGoals.mean()

    away_avg_shots = AwayTeamAwayShots.mean()
    away_avg_shots_home = AwayTeamHomeShots.mean()

    away_avg_ontarget = AwayTeamAwayShotsTarget.mean()
    away_avg_ontarget_home = AwayTeamHomeShotsTarget.mean()

    away_avg_fouls_home = AwayTeamHomeFouls.mean()
    away_avg_fouls_away = AwayTeamAwayFouls.mean()

    away_avg_ontarget_against = AwayTeamHomeShotsTargetAgainst.mean()

    away_avg_yellow = AwayTeamAwayYellows.mean()
    away_avg_yellow_home = AwayTeamHomeYellows.mean()

    away_avg_reds = AwayTeamAwayReds.mean()
    away_avg_reds_home = AwayTeamHomeReds.mean()

    away_shot_pg = AwayTeamAwayShots.mean() / AwayTeamAwayGoals.mean()
    away_shot_pg_home = AwayTeamHomeShots.mean() / AwayTeamHomeGoals.mean()
    return home_avg_goals, away_avg_goals

def getData(homeTeam,awayTeam):
    
    home_avg_goals,away_avg_goals = calculate(homeTeam,awayTeam)
        # Data to be written 
    dictionary ={ 
    "homeTeamName" : homeTeam,
    "awayTeamName" : awayTeam,
    "homeTeamGoals" : home_avg_goals,
    "awayTeamGoals" : away_avg_goals
    } 
        
    # Serializing json  
    json_object = json.dumps(dictionary, indent = 4) 
    return json_object