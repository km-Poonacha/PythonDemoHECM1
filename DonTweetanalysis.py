import csv

DONTWEETS_CSV = '/Users/medapa/Dropbox/HEC/Teaching/Python Sep 2016/Data/DONTWEETS_ana.csv'
NEW_DONTWEETS_CSV = '/Users/medapa/Dropbox/HEC/Teaching/Python Sep 2016/Data/NEW_DONTWEETS_ana.csv'
                                  
def main():        

    with open(DONTWEETS_CSV , 'rb') as don_tweets:
        tweet_read = csv.reader(don_tweets)
        prev_tweet_row = ['']
        tweet_count = 1
        with open(DONTWEETS_CSV , 'wb') as don_tweets_write:
            tweet_write = csv.writer(don_tweets_write)
            
            for tweet_row in tweet_read:
                if (tweet_row[8] != "Sat"  and tweet_row[8] != "Sun"):
                    if (tweet_row[8] == prev_tweet_row[8]):
                        
                    else:
                        
                        date = tweet_row[0]
                        DOW30_val = tweet_row[4]
                        NASDAQ_val= tweet_row[5]
                        CAC40_val= tweet_row[6]
                        MEXBOL_val = tweet_row[7]
                        
                        day_tweet_count = tweet_count

                        
                prev_tweet_row = tweet_row
                
            
            
        
if __name__ == '__main__':
  main()