from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json,time,csv
import pandas as pd
from nsetools import Nse

import Constants as con
import credentials as cr

# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """

    def __init__(self):
        self.counter = 0
        self.limit = 5
        pass

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = StdOutListener(fetched_tweets_filename)
        auth = OAuthHandler(cr.CONSUMER_KEY, cr.CONSUMER_SECRET)
        auth.set_access_token(cr.ACCESS_TOKEN, cr.ACCESS_TOKEN_SECRET)
        stream = Stream(auth, listener,tweet_mode='extended')

        # This line filter Twitter Streams to capture data by the keywords:
        stream.filter(track=hash_tag_list, languages=['en'],is_async=True,encoding='utf-8')


# # # # TWITTER STREAM LISTENER # # # #

class StdOutListener(StreamListener):
    """
    This is a basic listener that save received tweets to csv file.
    """

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            jsonData = json.loads(data)
            if "extended_tweet" in jsonData:
                text=jsonData['extended_tweet']['full_text']
            else:
                text = jsonData['text']
            createdAt = jsonData['created_at']

            # concatenate the timestamp with , and the text of the tweet
            saveThis = [createdAt,text.encode('utf-8')]

            # open file for writing, in append mode so that updates don't erase previous work
            with open(self.fetched_tweets_filename, 'a',encoding="utf-8") as tf:
                writer = csv.writer(tf)   #delimiter create extra newline so removed it
                writer.writerow(saveThis)
            return True

        except BaseException as e:
            print("Error on_data %s" % str(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    # nse = Nse()
    # all_stock_codes = nse.get_stock_codes(cached=True)
    # stock_codes = list(all_stock_codes.keys())
    # stock_names = list(all_stock_codes.values())
    # print(len(stock_names))
    # print("\n\ncompany codes\n")
    # print(stock_codes)
    # print("\n\ncompany names\n")
    # print(stock_names)

    # creating hash tag list of financial twitter feeds
    # hash_tag_list = [
    #     "bse",
    #     "nse",
    #     "nifty",
    #     "sensex",
    #     "Livemint",
    #     "ReutersIndia",
    #     "EconomicTimes",
    #     "Moneycontrol",
    #     "NDTVProfit",
    #     "SafalNiveshak",
    #     "BasantMaheshwari",
    #     "ForbesIndia",
    #     "BusinessStandard",
    #     "ETMarkets",
    #     "Investopedia",
    #     "CNBCTV18",
    #     "IndiaInfoline News",
    #     "NSEIndia",
    #     "ZeeBusiness",
    #     "investing", 
    #     "stocks", 
    #     "trading", 
    #     "stockmarket",
    #     "finance",
    #     "HDFC",
    #     "BHEL",
    #     "SBIN"
    # ]

    hash_tag_list_dict = con.hash_tag_list.values()
    hash_tag_list_list = list(hash_tag_list_dict)
    hash_tag_list = []
    for sublist in hash_tag_list_list:
        for item in sublist:
            hash_tag_list.append(item)
    print(hash_tag_list)
    fetched_tweets_filename = "new_tweets.csv"

    twitter_streamer = TwitterStreamer()

    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
