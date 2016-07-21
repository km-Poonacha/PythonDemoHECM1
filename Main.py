# Initialize tweepy and authorize

import tweepy
from tweepy import OAuthHandler
 
consumer_key = 'SKi8LqcB7sxQOEXfZwPzZuBWG'
consumer_secret = 'fct2RwHn7FQNl01xh45fH9T4QxLDyve7O4WURZzf5XFxyOVcVj'
access_token = '90844107-eW3IeYLpOY58rJkDyuVd85ZFxEHqTxljaFuPEsQnk'
access_secret = 'gZuRhIwSio4ZcnEvPGmw9IkhofJhoLFXs8PE8UDAG97yY'
 

def main():
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)  
    api = tweepy.API(auth)

# Get the tweets from realDonaldTrump
    for status in tweepy.Cursor(api.user_timeline, id= 'realDonaldTrump').items(10):
    # Process a single status
        print(status._json) 

main()        
