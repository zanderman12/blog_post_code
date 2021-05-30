# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 09:10:10 2021

@author: alext
"""

import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
import numpy as np

import sys
sys.path.insert(0, 'C:/Users/alext/Documents/GitHub/Python Scripts')
import read_google_sheet as rgs

def load_gsheet_data(gsheet_id, gsheet_sheet, length_of_gsheet):
    gsheet = rgs.get_google_sheet(gsheet_id, gsheet_sheet)
    gdf = rgs.gsheet2df(gsheet, length_of_gsheet)  
    return gdf

def get_info(attribute_dict, url, a):
    try:
        return attribute_dict[url][a]
    except:
        return None

if __name__ == '__main__':
    
    df = load_gsheet_data('10DNAdNNxhHNXvn2MyWFPaxRIIHSXvMiJSuw5eIwmOuA',
                          'Sheet2',200)
    
    attribute_dict = {}
    for BASE_URL in df['breed info link']:
        attribute_dict[BASE_URL] = {}
        res = requests.get(BASE_URL)
        if res.ok:
            soup = BS(res.content, 'html.parser')
            table = soup.find_all('ul')
            
            for t in table:
                
                if 'Temperament' in t.text and 'Height' in t.text:
                    li = t.find_all('li')
                    for l in li: 
                        a = l.text.split(':')
                        attribute_dict[BASE_URL][a[0]] = a[1]
                        
                       
    
                       
    #%%
    import numpy as np
    import re 
    
    df['temperament'] = df['breed info link'].apply(lambda x: get_info(attribute_dict,x,'\nTemperament')[1:-1].split(', '))
    df['akc breed popularity'] = df['breed info link'].apply(lambda x: get_info(attribute_dict,x,'\nAKC Breed Popularity'))
    df['height'] = df['breed info link'].apply(lambda x: get_info(attribute_dict,x,'\nHeight'))
    df['weight'] = df['breed info link'].apply(lambda x: get_info(attribute_dict,x,'\nWeight'))
    df['life_exp'] = df['breed info link'].apply(lambda x: get_info(attribute_dict,x,'\nLife Expectancy'))
    df['breed_group'] = df['breed info link'].apply(lambda x: get_info(attribute_dict,x,'\nGroup').split('\n')[1])
                    
    def clean_hw(hw):
        print(hw)
        if hw:
            nums = re.findall('\d+\.*\d*', hw)
            numlist = [float(n) for n in nums]
            print(numlist)
            return np.mean(numlist)
        else:
            return None
       
    df['height_inches'] = df.height.apply(lambda x: clean_hw(x))
    df['weight_pounds'] = df.weight.apply(lambda x: clean_hw(x))
    df['life_exp_years'] = df.life_exp.apply(lambda x: clean_hw(x))