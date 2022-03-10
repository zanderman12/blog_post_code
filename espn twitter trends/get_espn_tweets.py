# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 18:37:04 2021

@author: alext
"""

import tweepy
import pandas as pd
import pickle
import GetOldTweets3 as got
import time
import requests
from bs4 import BeautifulSoup as bs

def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler('YOUR ACCESS CODES', 
                           'YOUR ACCESS CODES')
    auth.set_access_token('YOUR ACCESS CODES', 
                          'YOUR ACCESS CODES')
    
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []  
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name, count=200)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print(f"getting tweets before {oldest}")
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        print(f"...{len(alltweets)} tweets downloaded so far")
    
    #transform the tweepy tweets into a 2D array that will populate the csv 
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]
    
    return outtweets



if __name__ == '__main__':
    
    file1 = open('twitter-@textfiles', 'r')

    data = []
    urls = []
    for line in file1.readlines():
        urls.append(line[-1])
        a = line.split('/')
        data.append(int(a[-1]))
        
    #%%
    auth = tweepy.OAuthHandler('YOUR ACCESS CODES', 
                           'YOUR ACCESS CODES')
    auth.set_access_token('YOUR ACCESS CODES', 
                          'YOUR ACCESS CODES')
    
    api = tweepy.API(auth, wait_on_rate_limit = True)
    
    tweetdata = []
    count = 0
    for i in data:
        try:
            t = api.get_status(i)
            row = [i, t.created_at, t.text, t.retweet_count, t.favorite_count, t.retweeted]
            tweetdata.append(row)
            count += 1
            print(count)
        except:
            print(count)
            break
        
        
    
    df = pd.DataFrame(data = tweetdata, 
                       columns = ['tid', 'date', 'text',  
                                  'num_retweets', 'num_likes', 'retweet'])
    
    pickle.dump(df, open('espn_tweets_' + str(count) + '.pickle', 'wb'))
    
