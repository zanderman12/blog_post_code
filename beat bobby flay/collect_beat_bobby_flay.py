# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 15:23:08 2021

@author: alext
"""
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as BS
import requests
import pickle


if __name__ == '__main__':
    BASE_URL = "https://en.wikipedia.org/wiki/Beat_Bobby_Flay"
    
    #request the raw html
    res = requests.get(BASE_URL)
    dfs = []
    if res.ok:
        
        #parse the raw html into beautiful soup
        soup = BS(res.content, 'html.parser')
        #find all the tables
        tables = soup.find_all('table')
        
        #loop through the tables which contain episode details (the others have other content)
        for table in tables[1:-2]:
            #read table into pandas datafrome
            df = pd.read_html(str(table))[0]
            
            #merge the multilevel column names into a single name
            df.columns = ['%s%s' % (a, '|%s' % b if b else '') for a, b in df.columns]
            dfs.append(df)
            
    #combine the dataframes into a single dataframe
    df = pd.concat(dfs)
    
    #rename columns into ones that make sense
    df.columns = ['show_num', 'epi_num', 'title', 'date', 'guests', 'first_ingredient', 'contestants', 'judges', 'main_dish', 'winner']
    
    #save dataframe
    df.to_csv('bbb.csv')