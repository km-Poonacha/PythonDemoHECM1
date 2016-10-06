#The following link details how we can get twitter archive data using the tweepy  https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/ 

#Installations required -  $pip install tweepy, 
#Installed $ pip install yahoo-finance. However before i could do it i needed to export $ CC=gcc
# Initialize tweepy and authorize

import tweepy
from tweepy import OAuthHandler
import json
import csv
from yahoo_finance import Share
from pandas_datareader import data, wb
import pandas_datareader.data as web

from datetime import date
from datetime import datetime
from datetime import time

# The following consumer ker and secret is my twitter feeds. you need to generate your consumer key and secrets for your twitter account. This is part of the OAuth security feature thatmost APIs use. 
# you should be able to get enough documentation online to do this 
consumer_key = 'XXX'
consumer_secret = 'XXX'
access_token = 'XXX'
access_secret = 'XXX'

DONTWEETS_CSV = '/Users/medapa/Dropbox/HEC/Teaching/Python Sep 2016/Data/DONTWEETS.csv' #<< You will need to edit this link to point it to your CSV file>>
DONTWEETS_WORDS_CSV = '/Users/medapa/Dropbox/HEC/Teaching/Python Sep 2016/Data/DONTWEETSWRDS.csv' # This file is used to calculate the word count for all the tweets

def get_index(index):
    #"""This function searches yahoo finance and gets the index values. Trump anounced his candidacy for president on June 16 2015. So we start the tweet analysis fro mthe 16th.""" 
    start = datetime(2015,06,16)
    end = date.today()
    index_data = web.DataReader(str(index), 'yahoo', start, end)
    return index_data
    
    
def collect_tweets(no_tweets):
    #"""This function finds the donald trump tweets and stores the collected data in a CSV file. It also finds the financial index data from yahoo-finance"""
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)  
    api = tweepy.API(auth)
#get index data and store in respective lists 
    DOW30 = get_index("^DJI")
    NASDAQ = get_index("^IXIC") 
    CAC40 = get_index("^FCHI")
    MEXBOL = get_index("^MXX")   
    prev_tweet_date = ''
    tweet_count = 1
# Get the tweets from realDonaldTrump
    for status in tweepy.Cursor(api.user_timeline, id= 'realDonaldTrump').items(no_tweets):
#Encode to utf8. This is done to avoid some errors that emerge when the data in the tweets have characters that are not utf8
        if status._json['text'] is None:
            tweet_text = ''                    
        else: 
            tweet_text = status._json['text'].encode('utf8', 'replace')  
        
        reply_uid = status._json['in_reply_to_user_id'] 
        reply_stateid = status._json['in_reply_to_status_id']
#Reformat tweet date using datetime. We need convert the date of the tweet to a format that CSV files can understand well 
        date1 =  str(status._json['created_at'])        
        tweet_date = datetime.strptime(date1[:20]+date1[26:30],'%a %b %d %H:%M:%S %Y')  
        
# Get the stock index data specific to the tweet date. Also note that stock index data is not available for sat and sun      
        if (date1[:3] != 'Sun' and date1[:3] != 'Sat') and (str(tweet_date.date()) != prev_tweet_date):
            print date1[:3] 
            prev_tweet_date = str(tweet_date.date())
            print "current tweet date", tweet_date.date()
            print "prev tweet", prev_tweet_date
            
            try:
                DOW30_val = (DOW30.Close[str(tweet_date.date())] - DOW30.Open[str(tweet_date.date())])/DOW30.Open[str(tweet_date.date())]
            except:
                print "EXCEPTION KEY ERROR AT DOW30_val date",str(tweet_date.date())
                DOW30_val = ''
                
            try:
                NASDAQ_val = (NASDAQ.Close[str(tweet_date.date())] - NASDAQ.Open[str(tweet_date.date())])/NASDAQ.Open[str(tweet_date.date())]
            except:
                print "EXCEPTION KEY ERROR AT NASDAQ_val date",str(tweet_date.date())
                NASDAQ_val = ''
             
            try: 
                CAC40_val = (CAC40.Close[str(tweet_date.date())] - CAC40.Open[str(tweet_date.date())])/CAC40.Open[str(tweet_date.date())]
            except:
                print "EXCEPTION KEY ERROR AT CAC40_val date",str(tweet_date.date())
                CAC40_val = ''
                         
            try:
                MEXBOL_val = (MEXBOL.Close[str(tweet_date.date())] -MEXBOL.Open[str(tweet_date.date())])/MEXBOL.Open[str(tweet_date.date())]
            except:
                print "EXCEPTION KEY ERROR AT MEXBOL_val date",str(tweet_date.date())
                MEXBOL_val =''
            day_tweet_count = tweet_count
            tweet_count = 1
            
        else:
            DOW30_val = ''
            NASDAQ_val = ''
            CAC40_val = ''
            MEXBOL_val = ''
            day_tweet_count = ''
            tweet_count = tweet_count + 1
            

#Store relavent information in csv        
        with open(DONTWEETS_CSV , 'ab') as don_tweets:
            tweet_write = csv.writer(don_tweets)
            tweet_write.writerow([status._json['created_at'],tweet_text,status._json['favorite_count'],status._json['retweet_count'],DOW30_val,NASDAQ_val,CAC40_val,MEXBOL_val,day_tweet_count ])
                   
    return
    
def word_count(word): 
    #"""This function counts the number of times a word has been used""" 
    with open(DONTWEETS_CSV , 'rb') as don_tweets:
        tweet_read = csv.reader(don_tweets)
        no_words = 0

        for tweet_row in tweet_read:
            word_list = str.split(tweet_row[1].lower())
            for tweet_words in word_list:
                if tweet_words == word:
                    no_words = no_words +1

        return no_words

def word_index():
    #"""This function finds all the words used and its count and stores them in a CSV"""
    with open(DONTWEETS_CSV , 'rb') as don_tweets:
        tweet_read = csv.reader(don_tweets)
        counting_words = [''] 
        del counting_words[:]  
        for tweet_row in tweet_read:
            word_list = str.split(tweet_row[1].lower())
            for word_list_i in word_list:
                word_done = 0
                for counting_words_i in counting_words:
                    if word_list_i == counting_words_i:
                        word_done = 1
                        break
                    else:
                        word_done = 0
                        continue
                if word_done == 0:
                    counting_words.append(word_list_i)
                    count = word_count(word_list_i)
                    if count > 100:
                        with open(DONTWEETS_WORDS_CSV , 'ab') as don_tweets_words:
                            tweet_words_write = csv.writer(don_tweets_words)
                            tweet_words_write.writerow([word_list_i,count])
                    
        
                                  
def main():        
    #"""This is the main function that calls the relevant functions and collect the data required. """
    tweets = 15000
# The following function collects the tweets and financial index data
    collect_tweets(tweets)
# The following function identifies the count of the individual words used in the tweets
    word_index()
# You can also individually calculate the the word count for a particular word    
    print word_count('you')

if __name__ == '__main__':
  main()