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

consumer_key = 'SKi8LqcB7sxQOEXfZwPzZuBWG'
consumer_secret = 'fct2RwHn7FQNl01xh45fH9T4QxLDyve7O4WURZzf5XFxyOVcVj'
access_token = '90844107-eW3IeYLpOY58rJkDyuVd85ZFxEHqTxljaFuPEsQnk'
access_secret = 'gZuRhIwSio4ZcnEvPGmw9IkhofJhoLFXs8PE8UDAG97yYX'

DONTWEETS_CSV = '/Users/medapa/Dropbox/HEC/Teaching/Python Sep 2016/Data/DONTWEETS.csv'

def get_index(index):
#This function searches yahoo finance and gets the index values 
# Trump anounced his candidacy for president on June 16 2015
    start = datetime(2015,06,16)
    end = date.today()
    index_data = web.DataReader(str(index), 'yahoo', start, end)
    return index_data
    
    
def collect_tweets(no_tweets):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)  
    api = tweepy.API(auth)
#get index data and store in respective lists 
    DOW30 = get_index("^DJI")
    NASDAQ = get_index("^IXIC") 
    FTSE100 = get_index("^FTSE")
    CAC40 = get_index("^FCHI")
    EURO50 = get_index("^STOXX50E")
#    DOWSH = get_index("^DJSH")
    MEXBOL = get_index("^MXX")   

    print date.today()
    print DOW30
    print NASDAQ
    print FTSE100
    print CAC40
    print EURO50
    print MEXBOL

# Get the tweets from realDonaldTrump
    for status in tweepy.Cursor(api.user_timeline, id= 'realDonaldTrump').items(no_tweets):
#Encode to utf8
        if status._json['text'] is None:
            tweet_text = ''                    
        else: 
            tweet_text = status._json['text'].encode('utf8', 'replace')  
        
        if status._json['in_reply_to_user_id'] is None:
            reply_uid = ''                    
        else: 
            reply_uid = status._json['in_reply_to_user_id'].encode('utf8', 'replace') 

        if status._json['in_reply_to_status_id'] is None:
            reply_stateid = ''                    
        else: 
            reply_stateid = status._json['in_reply_to_status_id'].encode('utf8', 'replace') 

#Reformat tweet date using datetime
        date1 =  str(status._json['created_at'])        
        tweet_date = datetime.strptime(date1[:20]+date1[26:30],'%a %b %d %H:%M:%S %Y')  
        prev_tweet_date = ''
# Get the index data specific to the tweet date       
        if (date1[:3] != 'Sun' and date1[:3] != 'Sat') and (str(tweet_date.date()) != prev_tweet_date)and (str(tweet_date.date()) != '2016-07-21')  :
            print date1[:3] 
            print tweet_date.date()
            DOW30_val = (DOW30.Close[str(tweet_date.date())] - DOW30.Open[str(tweet_date.date())])/DOW30.Open[str(tweet_date.date())]
            NASDAQ_val = (NASDAQ.Close[str(tweet_date.date())] - NASDAQ.Open[str(tweet_date.date())])/NASDAQ.Open[str(tweet_date.date())]
#            FTSE100_val = FTSE100.ix[str(tweet_date.date())]
            CAC40_val = (CAC40.Close[str(tweet_date.date())] - CAC40.Open[str(tweet_date.date())])/CAC40.Open[str(tweet_date.date())]
            EURO50_val= (EURO50.Close[str(tweet_date.date())] - EURO50.Open[str(tweet_date.date())])/EURO50.Open[str(tweet_date.date())]
#            DOWSH_val = DOWSH.ix[str(tweet_date.date())]
            MEXBOL_val = (MEXBOL.Close[str(tweet_date.date())] -MEXBOL.Open[str(tweet_date.date())])/MEXBOL.Open[str(tweet_date.date())]
            prev_tweet_date = str(tweet_date.date())
        else:
            DOW30_val = ''
            NASDAQ_val = ''
            FTSE100_val = ''
            CAC40_val = ''
            EURO50_val= ''
#            CHINAA50_val = ''
            MEXBOL_val = ''
            

#Store relavent information in csv        
        with open(DONTWEETS_CSV , 'ab') as don_tweets:
            tweet_write = csv.writer(don_tweets)
            tweet_write.writerow([status._json['created_at'],tweet_text,status._json['favorite_count'],status._json['retweet_count'],reply_uid,reply_stateid,DOW30_val,NASDAQ_val,FTSE100_val,CAC40_val,EURO50_val,MEXBOL_val ])
                   
    return
                
def main():        
# mention the number of tweets required
    tweets = 100
    collect_tweets(tweets)
    
if __name__ == '__main__':
  main()