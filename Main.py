#Installations required - $pip install googlefinance, $pip install tweepy, 

# Initialize tweepy and authorize

import tweepy
from tweepy import OAuthHandler
import json
import csv
from yahoo_finance import Share

consumer_key = 'SKi8LqcB7sxQOEXfZwPzZuBWG'
consumer_secret = 'fct2RwHn7FQNl01xh45fH9T4QxLDyve7O4WURZzf5XFxyOVcVj'
access_token = '90844107-eW3IeYLpOY58rJkDyuVd85ZFxEHqTxljaFuPEsQnk'
access_secret = 'gZuRhIwSio4ZcnEvPGmw9IkhofJhoLFXs8PE8UDAG97yY'

DONTWEETS_CSV = '/Users/medapa/Dropbox/HEC/Teaching/Python Sep 2016/Data/DONTWEETS.csv'

def collect_tweets(no_tweets):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)  
    api = tweepy.API(auth)

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

#Store relavent information in csv        
        with open(DONTWEETS_CSV , 'ab') as don_tweets:
            tweet_write = csv.writer(don_tweets)
            tweet_write.writerow([status._json['created_at'],tweet_text,status._json['favorite_count'],status._json['retweet_count'],reply_uid,reply_stateid ])
                                
    return
                
def main():        
# mention the number of tweets required
    tweets = 100
    collect_tweets(tweets)
    
    
    
if __name__ == '__main__':
  main()