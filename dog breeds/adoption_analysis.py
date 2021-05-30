# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 11:51:43 2021

@author: alext
"""

import pickle
import pandas as pd
import numpy as np

if __name__ == '__main__':
    
    a = pd.read_csv('train.csv')
    # b = pd.read_csv('test.csv')
    
    a = a[(a.AnimalType == 'Dog')]
    a['adopted'] = a.OutcomeType == 'Adopted'
    a['date'] = a.DateTime.apply(lambda x: pd.Timestamp(x))
    
    b = pickle.load(open('dog_breed_data.pickle', 'rb'))
    
    data = []
    for rrow in a.iterrows():
        r = rrow[1]
        height = []
        weight = []
        life_exp = []
        temperament = []
        for brow in b.iterrows():
            br = brow[1]
            breed = br.breed.replace('(', '').replace('(', '').split(' ')
            matching_breed = True
            for b in breed:
                if b not in r.Breed:
                    matching_breed = False
                    
            if matching_breed:
                height.append(br.height_inches)
                weight.append(br.weight_pounds)
                life_exp.append(br.life_exp_years)
                for t in br.temperament:
                    temperament.append(t)
        row = [r.breed, r.date, r.adopted, r.color, np.mean(height), np.mean(weight), 
               np.mean(life_exp), temperament]
        
        
    # df = pd.concat(a[['DateTime', 'AnimalType', 'Breed', 'Color', ]])