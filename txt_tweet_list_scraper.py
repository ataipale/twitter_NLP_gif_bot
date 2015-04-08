# this is my class for making a .txt list of tweets based 
# on user input of a search word and number of tweets to search 

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import Cursor
import sys
import os
import tweepy
import lda
import operator
import pudb
import json


#Set Twitter authentication keys
ckey = os.environ.get('CKEY')
ctoken = os.environ.get('CTOKEN')
atoken = os.environ.get('ATOKEN')
asecret = os.environ.get('ASECRET')

auth = OAuthHandler(ckey, ctoken)
auth.set_access_token(atoken, asecret)

#Using Twitter Python API wrapper
#retry_count tells the API to not try again when it fails
#originally this was unnecessary but after downloading the sample random tweets, something
#got messed up and after implementng this it fixed itself
api = tweepy.API(auth, retry_count=0, wait_on_rate_limit=True)

q = raw_input("What word would you like to search twitter for? ").lower()
max_tweets = int(raw_input("How many tweets would you like to search? ").lower())

filename = "tweets_about_" + q + '.txt'
# add to preexisting data file if it is a file
tweetTxtObject = open(filename, 'a')

#initiate dictionary to store counts of words 
wordCount = {}

# iterate through Tweepy's cursor function to gather latest tweets 
# convert each status to an ascii string
# add the tweet to a .txt file named after the search word
# 
with open('rate_limit.json', 'w') as outfile:
    json.dump(api.rate_limit_status(), outfile, sort_keys=True, indent=4)


for status in tweepy.Cursor(api.search, q).items(max_tweets):
    stringStatus = status.text.encode('ascii', 'ignore')
    tweetTxtObject.write(stringStatus)




