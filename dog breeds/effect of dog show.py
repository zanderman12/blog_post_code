# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 11:15:22 2021

@author: alext
"""

import pickle
import pandas as pd
import numpy
import seaborn as sns
import matplotlib.pyplot as plt

def num2str(x):
    try:
        return float(x)
    except:
        return None
    
    
if __name__ == '__main__':
    df = pickle.load(open('dog_breed_data.pickle', 'rb'))
    
    for i in ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']:
        df[i] = df[i].apply(lambda x: num2str(x))
        
    for i in ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']:
        if i != '2013':
            df['d_'+i] = df[i] - df[str(int(i)-1)]
            
    data = []
    for rrow in df.iterrows():
        r = rrow[1]
        for y in ['2013', '2014', '2015', '2016', '2017', '2018', '2019']:
            if y in str(r['westminster winner']):
                row = [int(y), r['d_' + str(int(y) + 1)], True, 'westminster', r['breed']]
                
            elif y in str(r['akc winner']):
                row = [int(y), r['d_' + str(int(y) + 1)], True, 'akc', r['breed']]
            elif y in str(r['national dog show']):
                row = [int(y), r['d_' + str(int(y) + 1)], True, 'national', r['breed']]
            else:
                row = [int(y), r['d_' + str(int(y) + 1)], False, None, r['breed']]
                
            data.append(row)
            
    ddf = pd.DataFrame(data = data, columns = ['year', 'delta', 'winner', 'show', 'breed'])
    
    #%%
    sns.pointplot(x = 'winner', y = 'delta', data = ddf)
    
    #%%
    from pytrends.request import TrendReq
    pytrend = TrendReq(hl='en-US', tz=360)
    
    a = list(ddf[ddf.winner == True].breed.unique())
    
  
    pytrend.build_payload(
                         kw_list=a[:5],
                         timeframe='2013-01-01 2020-12-31',
                         geo='US')
    google_data1 = pytrend.interest_over_time()
        
    pytrend.build_payload(
                         kw_list=a[5:10],
                         timeframe='2013-01-01 2020-12-31',
                         geo='US')
    google_data2 = pytrend.interest_over_time()
    
    pytrend.build_payload(
                         kw_list=a[10:15],
                         timeframe='2013-01-01 2020-12-31',
                         geo='US')
    google_data3 = pytrend.interest_over_time()
    
    pytrend.build_payload(
                         kw_list=a[15:],
                         timeframe='2013-01-01 2020-12-31',
                         geo='US')
    google_data4 = pytrend.interest_over_time()
        
#%%
    from scipy.stats import zscore
    a = pd.merge(google_data1, google_data2, left_index = True, right_index = True)
    b = pd.merge(google_data3, google_data4, left_index = True, right_index = True)
    
    gdf = pd.merge(a, b, left_index = True, right_index = True).reset_index()
    
    
    
    for d in list(ddf[ddf.winner == True].breed.unique()):
        sns.lineplot(x = gdf.date, y = zscore(gdf[d]))
        
    #%%
    
    dfs = []
    for d in list(ddf[ddf.winner == True].breed.unique()):
        a = gdf[['date', d]].copy()
        a.columns = ['date', 'gtrend']
        a['breed'] = d
        a['z_gtrend'] = zscore(a.gtrend)
        dfs.append(a)
        
    gdf = pd.concat(dfs, axis = 0)
    
    #%%
    
    
                