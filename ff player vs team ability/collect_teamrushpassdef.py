# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 19:32:01 2021

@author: alext
"""

import requests
import urllib.request
from bs4 import BeautifulSoup as BS
import pandas as pd
import numpy as np
import pickle
from scipy.stats import linregress

def get_fantasy_data():
    dfs = []
    url = 'https://www.pro-football-reference.com'
    for y in range(2015, 2021):
        
    
        r = requests.get(url + '/years/' + str(y) + '/fantasy.htm')
        soup = BS(r.content, 'html.parser')
        parsed_table = soup.find_all('table')[0]  
        
        df = pd.read_html(str(parsed_table))[0]
        df['year'] = y
        
        dfs.append(df)
        
    df = pd.concat(dfs)
    df.columns = ['rk', 'player', 'tm', 'fantpos', 'age', 'g', 'gs', 'cmp', 
                  'pass_att', 'pass_yds', 'pass_tds', 'ints', 'rush_att', 
                  'rush_yds', 'rush_ypera', 'rush_td', 'rec_tgt', 'rec_rec', 'rec_yds', 
                  'rec_yperr', 'rec_td', 'fmb', 'fmb_l', 'td', '2pm', '2pp', 'fantpt', 'ppr', 
                  'dkpt', 'fdpt', 'vbd', 'posrank', 'ovrank', 'year']
    
    df = df[df.rk != 'Rk']
    for c in ['rk', 'age', 'g', 'gs', 'cmp', 'pass_att', 'pass_yds', 'pass_tds', 'ints', 'rush_att', 
                  'rush_yds', 'rush_ypera', 'rush_td', 'rec_tgt', 'rec_rec', 'rec_yds', 
                  'rec_yperr', 'rec_td', 'fmb', 'fmb_l', 'td', '2pm', '2pp', 'fantpt', 'ppr', 
                  'dkpt', 'fdpt', 'vbd', 'posrank', 'ovrank']:
        df[c] = df[c].astype(float)
    
    return df
  
def get_teamskill():
    passdfs = []
    rushdfs = []
    for y in ['2015', '2016', '2017', '2018', '2019', '2020']:
                
        passdf = pd.read_excel('historicalpassrush.xls', sheet_name = y + ' passing')
        
        passdf['year'] = int(y)
        passdfs.append(passdf)
        
        rushdf = pd.read_excel('historicalpassrush.xls', sheet_name = y + ' rushing')
        rushdf['year'] = int(y)
        rushdfs.append(rushdf)
        
    passdf = pd.concat(passdfs)
    rushdf = pd.concat(rushdfs)
    
    df = passdf[['Tm', 'EXP', 'year']].merge(rushdf[['Tm', 'EXP', 'year']], on = ['Tm', 'year'], suffixes = ('_pass', '_rush'))

    return df

def clean_team(x):
    t = ''
    for i in x:
        if i not in ['*', '+']:
            t += i
    return t
def get_teamoffdef():
    dfs = []
    for y in range(2015, 2021):
        url = 'https://www.pro-football-reference.com/years/' + str(y) + '/'
        r = requests.get(url)
        soup = BS(r.content, 'html.parser')
        parsed_table = soup.find_all('table')
        
        df = pd.read_html(str(parsed_table))[0]
        df = df[~df.Tm.isin(['AFC East', 'AFC West', 'AFC North', 'AFC South'])]
        df['year'] = y
        dfs.append(df)
        df = pd.read_html(str(parsed_table))[1]
        df = df[~df.Tm.isin(['NFC East', 'NFC West', 'NFC North', 'NFC South'])]
        df['year'] = y
        dfs.append(df)
    
    df = pd.concat(dfs)
    df['tm'] = df.Tm.apply(lambda x: clean_team(x))
    for c in [ 'W', 'L', 'W-L%', 'PF', 'PA', 'PD', 'MoV', 'SoS', 'SRS', 'OSRS',
       'DSRS']:
        df[c] = df[c].astype(float)
    
    return df
    

if __name__ == '__main__':
    
    
    teamdf = get_teamoffdef()
    fantdf = get_fantasy_data()
    prdf = get_teamskill()


    teamdict = {'New Orleans Saints': 'NOR', 'Arizona Cardinals': 'ARI', 'Pittsburgh Steelers': 'PIT',
        'San Diego Chargers': 'SDG', 'New England Patriots': 'NWE', 'Atlanta Falcons':'ATL',
        'New York Giants':'NYG', 'Baltimore Ravens':'BAL', 'Detroit Lions':'DET',
        'Jacksonville Jaguars':'JAX', 'Washington Redskins':'WAS',
        'Philadelphia Eagles':'PHI', 'New York Jets':'NYJ', 'Denver Broncos':'DEN',
        'Cincinnati Bengals':'CIN', 'Oakland Raiders':'OAK', 'Tampa Bay Buccaneers':'TAM',
        'Houston Texans':'HOU', 'Miami Dolphins':'MIA', 'Seattle Seahawks':'SEA',
        'Cleveland Browns':'CLE', 'Indianapolis Colts':'IND', 'Chicago Bears':'CHI',
        'Carolina Panthers':'CAR', 'Tennessee Titans':'TEN', 'Green Bay Packers':'GNB',
        'Dallas Cowboys':'BAL', 'Buffalo Bills':'BUF', 'San Francisco 49ers':'SFO',
        'Kansas City Chiefs':'KAN', 'Minnesota Vikings':'MIN', 'St. Louis Rams':'STL',
        'Los Angeles Rams':'LAR', 'Los Angeles Chargers':'LAC', 'Las Vegas Raiders':'LVR',
        'Washington Football Team':'WAS'}
    
    prdf['cleanteam'] = prdf.Tm.map(teamdict)
    teamdf['cleanteam'] = teamdf.tm.map(teamdict)
    df = fantdf.merge(prdf, left_on = ['tm', 'year'], right_on = ['cleanteam', 'year'])

    df = df.merge(teamdf[['cleanteam', 'year', 'OSRS', 'DSRS', 'SoS']], left_on = ['tm', 'year'], right_on = ['cleanteam', 'year'])
    #%%
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    fig, axs = plt.subplots(1,3)
    ps = ['QB', 'WR', 'TE']
    for i in range(3):
        gdf = df[(df.fantpos == ps[i]) & (df.posrank < 20)]
        sns.regplot(ax = axs[i], x = 'EXP_rush', y = 'ppr', data = gdf)
        axs[i].set_xlabel('Expected Points from Rushing')
        axs[i].set_ylabel('Fantasy Points')
        axs[i].set_title(ps[i])
        
        print(linregress(gdf.EXP_rush, y = gdf.ppr))
    
    #%%
    
    plt.figure()
    sns.regplot(x = 'EXP_pass', y = 'ppr', data = df[(df.fantpos == 'RB') & (df.posrank < 20)])
    plt.title("RB Fantasy Points vs Team's Expected Points from Passing")
    plt.xlabel('Expected Points from Passing')
    plt.ylabel('Fantasy Points')
    
    gdf = df[(df.fantpos == 'RB') & (df.posrank.between(0,20))]
    
    a = linregress(gdf.EXP_pass, gdf.ppr)
    
    #%%
  
    plt.figure()
    for p in ['QB']:
        sns.regplot(x = 'DSRS', y = 'ppr', data = df[(df.fantpos == p) & (df.posrank.between(6,18))])
        
    gdf = df[(df.fantpos == p) & (df.posrank.between(6,18))]
    
    a = linregress(gdf.DSRS, gdf.ppr)
    
    plt.title('QB Fantasy Performance relative to Team Defense')
    plt.ylabel('Fantasy Points')
    plt.xlabel('Defensive Rating')
    # plt.legend(['QB', 'WR', 'TE'])