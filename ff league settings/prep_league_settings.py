# -*- coding: utf-8 -*-
"""
Created on Tue May  4 07:53:36 2021

@author: alext
"""
import pandas as pd
import numpy as np
import pickle
import seaborn as sns
import matplotlib.pyplot as plt

def fpoints(row, ppr = 0, passtd = 4, passyrds = 0.04, 
            te_ppr = 0, ptcarry = 0, intval = -2):
        
        total = 0
        total += int(row.pass_yds) * passyrds
        total += int(row.pass_tds) * passtd
        total += int(row.ints) * intval
        total += int(row.rush_att) * ptcarry
        total += int(row.rush_yds) * 0.1
        total += int(row.rush_td) * 6
        if row.fantpos == 'TE':
            total += int(row.rec_rec) * (ppr + te_ppr)
        else:
            total += int(row.rec_rec) * ppr
            
        total += int(row.rec_yds) * 0.1
        total += int(row.rec_td) * 6
        total -= int(row.fmb_l) * 2
        total += int(row['2pm']) * 2
        total += int(row['2pp']) * 2
        
        return total

if __name__ == '__main__':
    
    df = pickle.load(open('fantasy_history.pickle','rb'))
    df = df[df.player != 'Player']
    df.fillna(0, inplace = True)
    df.reset_index()
    
    fulldata = []
    errors = []
    for ppr in [0,0.5,0.75,1]:
        for ptd in [4,6]:
            for pyrd in [1/10, 1/15, 1/20, 1/25]:
                for tepr in [0,0.5,1]:
                    for pc in [0, 0.25, 0.5]:
                        for intval in [-2, -3, -4]:
                            df['total_points'] = df.apply(lambda x: fpoints(x, ppr, ptd, pyrd, tepr, pc, intval), axis = 1)
                            for numteams in [8,10,12]:
                                for y, ydf in df.groupby('year'):
                                    for qbs in [1,2]:
                                        for rbs in [2]:
                                            for wrs in [2,3]:
                                                for tes in [1]:
                                                    for rw in [0,1]:
                                                        for rwt in [0,1,2]:
                                                            for qrwt in [0,1]:
                                                                # try: 
                                                                    data = []
                                                                    included_players = []
                                                                    rprank = {'QB':qbs, 
                                                                              'RB':rbs, 
                                                                              'WR':wrs, 
                                                                              'TE':tes, 
                                                                              'rw':rw,
                                                                              'rwt':rwt, 
                                                                              'qrwt':qrwt}
                                                                    
                                                                    row = [ppr, ptd, pyrd, tepr, pc, intval, numteams, y, qbs, rbs, wrs, tes, rw, rwt, qrwt]
                                                                    
                                                                    for pos in ['QB', 'RB', 'WR', 'TE', 'rw', 'rwt', 'qrwt']:
                                                                        if pos == 'rw':
                                                                            posdf = ydf[(ydf.fantpos.isin(['RB', 'WR'])) & (~ydf.index.isin(included_players))].copy()
                                                                        elif pos == 'rwt':
                                                                            posdf = ydf[(ydf.fantpos.isin(['RB', 'WR', 'TE'])) & (~ydf.index.isin(included_players))].copy()
                                                                        elif pos == 'qrwt':
                                                                            posdf = ydf[(ydf.fantpos.isin(['QB', 'RB', 'WR', 'TE'])) & (~ydf.index.isin(included_players))].copy()
                                                                        else:
                                                                            posdf = ydf[(ydf.fantpos == pos) & (~ydf.index.isin(included_players))].copy()
                                                                            
                                                                        
                                                                        posdf['posrank'] = posdf.total_points.rank(ascending = False, method = 'first')
                                                                        vorprank = numteams * rprank[pos] + 1
                                                                        posvorp = posdf[posdf.posrank == vorprank].iloc[0]['total_points']
                                                                        
                                                                        posdf['vorp'] = posdf.total_points - posvorp
                                                                        
                                                                        posdf = posdf.sort_values('posrank').iloc[:vorprank]
                                                                        
                                                                        for i in posdf.index:
                                                                            included_players.append(i)
                                                                            
                                                                        data.append(posdf[['player', 'fantpos', 'tm', 'total_points', 'posrank', 'vorp']])
                                                                        
                                                                        row.append(posdf.vorp.max())
                                                                        row.append(posdf.vorp.median())
                                                                    ddf = pd.concat(data)
                                                                    
                                                                    ddf = ddf.sort_values('vorp', ascending = False).iloc[:40]
                                                                    
                                                                    a = ddf.groupby('fantpos').count()
                                                                    
                                                                    for i in ['QB', 'RB', 'WR', 'TE']:
                                                                        try: 
                                                                            row.append(a.loc[i, 'player'])
                                                                        except:
                                                                            row.append(0)
                                                                        
                                                                    fulldata.append(row)
                                                                # except:
                                                                #     row = [ppr, ptd, numteams, y, qbs, rbs, wrs, tes, rw, rwt, qrwt]
                                                                #     errors.append(row)
                                                                #     continue
                                                
    ldf = pd.DataFrame(data = fulldata, columns = ['ppr', 'ptd', 'pyrd', 'tepr', 'pc', 'intval', 'numteams', 'year', 'qbs', 'rbs', 'wrs', 'tes', 'rw', 'rwt', 'qrwt',
                                                   'qb_maxvorp', 'qb_medvorp', 'rb_maxvorp', 'rb_medvorp', 'wr_maxvorp', 'wr_medvorp',
                                                   'te_maxvorp', 'te_medvorp', 'rw_maxvorp', 'rw_medvorp', 'rwt_maxvorp', 'rwt_medvorp', 
                                                   'qrwt_maxvorp', 'qrwt_medvorp', 'top40_qbs', 'top40_rbs', 'top40_wrs', 'top40_tes'])
                                                
    pickle.dump(ldf, open('scoring_sim_data.pickle', 'wb'))
#%%


data = []
for rrow in ldf.iterrows():
    r = rrow[1]
    for pos in ['qb', 'rb', 'wr', 'te']:
        row = [r.ppr, r.ptd, 1/r.pyrd, r.tepr, r.numteams, r.year, r.qbs, r.rbs, r.wrs, r.tes,
               r.rw, r.rwt, r.qrwt, pos, r[pos + '_maxvorp'], r[pos+'_medvorp'],
               r['top40_' + pos +'s']]
        data.append(row)
                                  
gdf = pd.DataFrame(data = data, columns = ['ppr', 'ptd', '1 pt per X passing yds', 'te ppr above base ppr', 'points per carry', 'interception value', '# of teams', 'year', 'qbs', 'rbs', 'wrs', 'tes', 'rb/wr', 'flex', 'superflex',
                                           'pos', 'maxvorp', 'medvorp', 'top40'])

#%%

sns.boxplot(x = 'pos', y = 'top40', hue = 'te premium', data = gdf)




        
                                                
                                                
                                                