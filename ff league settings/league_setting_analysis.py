# -*- coding: utf-8 -*-
"""
Created on Sun May  2 12:07:22 2021

@author: alext
"""
import pandas as pd
import numpy as np
import pickle
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == '__main__':
    
    df = pickle.load(open('player_value_by_league_settings.pickle','rb'))
    
    
    for p in ['QB', 'RB', 'WR', 'TE']:
        qb_df = df[df.pos == p]
        plt.figure()
        sns.regplot(x = 'rank', y = 'vorp', data = qb_df[qb_df.num_teams == 8], 
                    color = 'b', logx = True, scatter = False)
        sns.regplot(x = 'rank', y = 'vorp', data = qb_df[qb_df.num_teams == 10],
                    color = 'r', logx = True, scatter = False)
        sns.regplot(x = 'rank', y = 'vorp', data = qb_df[qb_df.num_teams == 12], 
                    color = 'g', logx = True, scatter = False)
        plt.legend(['8', '10', '12'])
        plt.axhline(y = 0, color = 'k')
        plt.title(p)
        
        #%%
    from scipy import optimize as op 
    
    data = []
    
    def curve(x, a, b):
        return a * np.exp((-1/b) * x)
    
    for p in ['QB', 'RB', 'WR', 'TE']:
        for ptd in [4, 6]:
            for n in [8, 10, 12]:
            
                a = df[(df.num_teams == n) & (df.pass_td == ptd) & (df.pos == p)]
                a.dropna(subset = ['rank', 'vorp'], how = 'any', inplace = True)
                xdata = a['rank']
                ydata = a.vorp
                popt, pcov = op.curve_fit(curve, xdata, ydata)
                
                b = a.groupby('year').max()
                c = a[a.vorp > 0].groupby('year').median()
                
                row = [p, ptd, n, popt[0], popt[1], pcov, b.vorp.mean(), c.vorp.mean(), popt[1]*np.log(2)]
                data.append(row)
    
    curve_df = pd.DataFrame(data = data, columns = ['pos', 'ptd', 'nteams', 'a', 'b', 
                                                    'pcov', 'max_vorp', 'u_vorp', 'half-life'])
    
    #%%
    a = qb_df[(qb_df.num_teams == 10) & (qb_df.vorp > 0) & (qb_df.pass_td == 4)]
    
    a['zvorp'] = (a.vorp - a.vorp.mean())/a.vorp.std()
    
    
    #%%
    rb_df = df[(df.pos == 'RB') & (df.pass_td == 4)].dropna(subset = ['rank', 'vorp'], how = 'any')
    popt, pcov = op.curve_fit(curve, rb_df['rank'], rb_df['vorp'])
    
    x = np.linspace(1,70,1000)
    y = curve(x, popt[0], popt[1])
    
    sns.scatterplot(x = 'rank', y = 'vorp', data = rb_df, alpha = 0.1, color = 'k')
    sns.lineplot(x = x, y = y, color = 'b')
    plt.legend(['test'])
    #%%
    for t in [8, 10, 12]: 
        rb_df = df[(df.pos == 'QB') & (df.pass_td == 4) & (df.num_teams == t)].dropna(subset = ['rank', 'vorp'], how = 'any')
        popt, pcov = op.curve_fit(curve, rb_df['rank'], rb_df['vorp'])
        
        x = np.linspace(1,70,1000)
        y = curve(x, popt[0], popt[1])
        
        sns.lineplot(x = x, y = y)
        
    plt.legend(['8', '10', '12'])
    
    #%%
    gdf = curve_df[(curve_df.pos == 'RB') & (curve_df.ptd == 4)]
    fig, axs = plt.subplots(1,3)
    axs[0].bar(gdf.nteams, height = gdf.max_vorp)
    axs[1].bar(gdf.nteams, height = gdf.u_vorp)
    axs[2].bar(gdf.nteams, height = gdf['half-life'])
    