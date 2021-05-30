# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 09:44:22 2021

@author: alext
"""

import pandas as pd
import pickle
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def num2str(x):
    try:
        return float(x)
    except:
        return None
    
def custom_round(x, base=5):
    try:
        return int(base * round(float(x)/base))
    except:
        return None

if __name__ == '__main__':
    
    df = pickle.load(open('dog_breed_data.pickle', 'rb'))
    
    nafill = {}
    for i in ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']:
        df[i] = df[i].apply(lambda x: num2str(x))
        df[i+'_weight'] = df[i].rank(ascending = False)
    df['delta_poprank'] = df['2020'] - df['2013']
    df['rd_height'] = df.height_inches.apply(lambda x: custom_round(x))
    df['rd_weight'] = df.weight_pounds.apply(lambda x: custom_round(x, base = 10))
    df['rd_lifexp'] = df.life_exp_years.apply(lambda x: custom_round(x, base = 3))
    data = []
    weighted_data = []
    temp_data = []
    for rrow in df.iterrows():
        r = rrow[1]
        for i in ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']:
            row = [r.breed, i, r[i], r[i+'_weight'], r.temperament, r.height_inches, r.weight_pounds, r.life_exp_years, r.breed_group]
            data.append(row)
            if pd.notnull(r[i+'_weight']):
                for j in range(int(r[i+'_weight'])):
                    row = [r.breed, i, r[i], r.temperament, r.height_inches, r.weight_pounds, r.life_exp_years, r.breed_group]
                    weighted_data.append(row)
            if np.all(pd.notnull(r.temperament)):
                for j in range(len(r.temperament)):
                    row = [r.temperament[j], i, r[i], r[i+'_weight'], r.height_inches, r.weight_pounds, r.life_exp_years, r.breed_group, r.delta_poprank]
                    temp_data.append(row)
    wdf = pd.DataFrame(data = weighted_data, columns = ['breed', 'year', 'poprank', 'temperament', 'height', 'weight', 'life_exp', 'breed_group'])
    ddf = pd.DataFrame(data = data, columns = ['breed', 'year', 'poprank', 'poprank_weight', 'temperament', 'height', 'weight', 'life_exp', 'breed_group'])
    tdf = pd.DataFrame(data = temp_data, columns = ['temperament', 'year', 'poprank', 'poprank_weight', 'height', 'weight', 'life_exp', 'breed_group', 'delta_poprank'])
    ddf.dropna(axis = 0, how ='any', inplace = True)
    wdf.dropna(axis = 0, how ='any', inplace = True)
    tdf.dropna(axis = 0, how ='any', inplace = True)

    
    #%%
    
    
    ddf['rd_height'] = ddf.height.apply(lambda x: custom_round(x))
    ddf['rd_weight'] = ddf.weight.apply(lambda x: custom_round(x, base = 10))
    ddf['rd_lifexp'] = ddf.life_exp.apply(lambda x: custom_round(x, base = 3))
    sns.pointplot(x = 'life_exp', y = 'poprank', hue = 'year', data = ddf[ddf.poprank < 50])
    
    #%%
    
    sns.pointplot(x = 'year', y = 'poprank', data = ddf[(ddf.poprank < 50) & (ddf.life_exp == 9.0)])
    
    #%%
    
    a = tdf.groupby('temperament').count().reset_index()
    a['temp_rank'] = a.year.rank(ascending = False)
    
    gdf = tdf[tdf.temperament.isin(a[a.temp_rank <= 20].temperament)]
    
    a = gdf.groupby('temperament').mean().reset_index().sort_values('delta_poprank', ascending = True)

    
    sns.pointplot(x = 'temperament', y = 'delta_poprank', data = gdf, order = a.temperament, join = False, scale = 2, linewidth = 2)
    # sns.swarmplot(x = 'temperament', y = 'poprank', data = gdf, order = a.temperament, alpha = 0.2)
    plt.xticks(rotation = -45)
    plt.ylabel('Change in Ranking', fontsize = 16)
    plt.title('Change in Breed Popularity by Temperament', fontsize = 20)
    plt.xlabel('Temperament', fontsize = 16)
    
    #%%
    
    sns.lineplot(x = 'year', y = 'poprank', hue = 'breed', data = ddf[ddf.breed.isin(['French Bulldogs', 'Yorkshire Terriers'])])
    plt.ylabel('Popularity Ranking')
    
    #%% selcect top 5 or 10 of each category
    
    ddf.sort_values('poprank', inplace = True)
    
    dfs = []
    metric = 'rd_weight'
    
    for y, ydf in ddf.groupby(['year', metric]):
        ydf['bg_rank'] = ydf.poprank.rank(ascending = True)
        dfs.append(ydf)
        
    gdf = pd.concat(dfs)
    
    sns.regplot(x = metric, y = 'poprank', data = gdf[gdf.bg_rank <=10])
    
    #%%
    
    dfs = []
    for b, bdf in ddf.sort_values('year', ascending = True).groupby('breed'):
        bdf['poprank_1'] = bdf.poprank.shift(-1)
        bdf['delta_poprank'] = bdf.poprank - bdf.poprank.shift(1)
        dfs.append(bdf)
        
    gdf = pd.concat(dfs)
    
    sns.violinplot(gdf[gdf.delta_poprank.abs() <= 10].delta_poprank)
    plt.xlabel('Change in Popularity')
    plt.ylabel('Number of Breeds')
    plt.title('Change in Popularity per Year')
            
    #%%
    
    metric = 'breed_group'
    
    a = df[[metric, 'delta_poprank']].groupby(metric).mean().reset_index().sort_values('delta_poprank', ascending = True)[metric]
    fig,ax = plt.subplots()
    fig.subplots_adjust(bottom=0.3)
    sns.pointplot(x = metric, y = 'delta_poprank', data = df, join = False, order = a)
    plt.xticks(rotation = -45)
    plt.ylabel('Change in Ranking', fontsize = 14)
    plt.title('Change in Breed Group Popularity', fontsize = 16)
    plt.xlabel('Breed Group', fontsize = 14)
    
    #%%
    wdf['rd_height'] = wdf.height.apply(lambda x: custom_round(x))
    wdf['rd_weight'] = wdf.weight.apply(lambda x: custom_round(x, base = 10))
    plt.hexbin(x = wdf.height, y = wdf.weight, gridsize = 10)
    plt.xlabel('Height in inches')
    plt.ylabel('Weight in pounds')
    
    
    
    
    