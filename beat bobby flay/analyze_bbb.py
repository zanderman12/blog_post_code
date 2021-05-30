# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 15:41:57 2021

@author: alext
"""


import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == '__main__':
    
    #load dataframe
    bdf =pd.read_csv('bbb.csv')
    
    #clean dataframe by celebrity guest
    guest_data = []
    for rrow in bdf.iterrows():
        gs = rrow[1]['guests'].split(', ')
        win = rrow[1]['winner'] != 'Bobby Flay'
        for g in gs:
            new_row = [g, win]
            guest_data.append(new_row)
      
    #create celebrity guest dataframe with number of wins and appearences
    gdf = pd.merge(pd.DataFrame(data = guest_data, columns = ['guest', 'win']).groupby('guest').sum(),
                   pd.DataFrame(data = guest_data, columns = ['guest', 'win']).groupby('guest').count(),
                   left_index = True, right_index = True)
        
    gdf.columns = ['wins', 'appearences']
    gdf.reset_index(inplace = True)
    
    #determine celebrity guest win rate
    gdf['winrate'] = np.round(gdf.wins / gdf.appearences * 100,1)
    gdf['losses'] = gdf.appearences - gdf.wins
    gdf['lossrate'] = 100 - gdf.winrate
    
    #%% create celebrity guest win rate chart
    
    a = gdf[(gdf.appearences >=5) & (gdf.winrate > 100-62.9)].sort_values('winrate', ascending = False)
    a['clean_guest'] = a.apply(lambda x: x.guest + ': ' + str(x.appearences), axis = 1)
    fig, ax = plt.subplots()
    ax.set_axisbelow(True)
    plt.grid(b =True, axis = 'y')
    sns.scatterplot(x = 'winrate', y = 'clean_guest', data = a, s = 5000, linewidth=1)
    i = 0
    for rrow in a.iterrows():
        
        ax.text(x=rrow[1].winrate, y=i, s=str(rrow[1].winrate) + '%', 
                fontsize=16, color='white', 
                horizontalalignment='center',
                fontweight='bold')
        i += 1
    
    plt.yticks(fontsize = 22)
    ax.axes.get_xaxis().set_visible(False)
    plt.title('Win Rate per Guest', fontsize = 28)
    
    
    #%% create star ingredient plot
    
    
    piedata = bdf.groupby('ing type')['show_num'].count().sort_values(ascending = False).reset_index()
    fig, ax = plt.subplots()
    ax.set_axisbelow(True)
    plt.grid(b =True, axis = 'y')
    sns.scatterplot(x = 'show_num', y = 'ing type', data = piedata, s = 5000, linewidth=1)
    i = 0
    for rrow in piedata.iterrows():
        
        ax.text(x=rrow[1].show_num, y=i, s=str(np.round(100*rrow[1].show_num / piedata.show_num.sum(),1)) + '%', 
                fontsize=16, color='white', 
                horizontalalignment='center',
                fontweight='bold')
        i += 1
    
    plt.yticks(fontsize = 22)
    ax.axes.get_xaxis().set_visible(False)
    plt.title('Star Ingredient Category', fontsize = 28)
    plt.ylabel('Ingredient Category', size = '24')
    
    #%% create cuisine, protein, or meal type chart
    cuisine_data = []
    for rrow in bdf.iterrows():
        c = rrow[1]['type'] #change this to be either cuisine, protein or meal type
        win = rrow[1]['winner'] != 'Bobby Flay'
        
        new_row = [c, win]
        cuisine_data.append(new_row)
            
    cdf = pd.merge(pd.DataFrame(data = cuisine_data, columns = ['cuisine', 'win']).groupby('cuisine').sum(),
                   pd.DataFrame(data = cuisine_data, columns = ['cuisine', 'win']).groupby('cuisine').count(),
                   left_index = True, right_index = True)
        
    cdf.columns = ['wins', 'appearences']
    cdf.reset_index(inplace = True)
    
    cdf['winrate'] = np.round(cdf.wins / cdf.appearences * 100,1)
    cdf['losses'] = cdf.appearences - cdf.wins
    cdf['lossrate'] = 100 - cdf.winrate
    
    a = cdf[(cdf.appearences >=5)].sort_values('winrate', ascending = False)
    a['clean_cuisine'] = a.apply(lambda x: x.cuisine + ': ' + str(x.appearences), axis = 1)
    fig, ax = plt.subplots()
    ax.set_axisbelow(True)
    plt.grid(b =True, axis = 'y')
    plt.axvline(x = 100-62.9, color = 'r')
    sns.scatterplot(x = 'winrate', y = 'clean_cuisine', data = a, s = 5000, linewidth=1)
    i = 0
    for rrow in a.iterrows():
        
        ax.text(x=rrow[1].winrate, y=i, s=str(rrow[1].winrate) + '%', 
                fontsize=16, color='white', 
                horizontalalignment='center',
                fontweight='bold')
        i += 1
    
    plt.yticks(fontsize = 22)
    ax.axes.get_xaxis().set_visible(False)
    plt.title('Win Rate By Meal Type', fontsize = 28)
    plt.ylabel('Signature Meal Type', fontsize = 24)
    
    
    
    
