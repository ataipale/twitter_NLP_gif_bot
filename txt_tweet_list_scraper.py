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
import textmining 

def processJsonData():
    data = []
    with open('sample_tweets2.json') as data_file:
        for line in data_file:
            data.append(json.loads(line))

    for item in data:
        status = item.get("text")
        # write the statuses as a string to a .txt doc
        filename = "sample_tweets2.txt"
        randomTweetObject = open(filename, 'w')
        if status:
            stringRandomTweet = status.encode('ascii', 'ignore')
            randomTweetObject.write(stringRandomTweet)

def create_TDM():
    doc1 = "sample_tweets2.txt"
    doc2 = "tweets_about_girl.txt"
    # Initialize class to create term-document matrix
    tdm = textmining.TermDocumentMatrix()
    # Add the documents
    tdm.add_doc(doc1)
    tdm.add_doc(doc2)
    # Write out the matrix to a csv file. Note that setting cutoff=1 means
    # that words which appear in 1 or more documents will be included in
    # the output (i.e. every word will appear in the output). The default
    # for cutoff is 2, since we usually aren't interested in words which
    # appear in a single document. For this example we want to see all
    # words however, hence cutoff=1.
    tdm.write_csv('matrix.csv', cutoff=1)
    # Instead of writing out the matrix you can also access its rows directly.
    # Let's print them to the screen.
    for row in tdm.rows(cutoff=1):
        print row

# write about rate limit data
def getRateLimit():
    with open('rate_limit.json', 'w') as outfile:
        json.dump(api.rate_limit_status(), outfile, sort_keys=True, indent=4)

def getStatuses(q, max_tweets, auth):    
    filename = "tweets_about_" + q + '.txt'
    # add to preexisting data file if it is a file
    tweetTxtObject = open(filename, 'a')

    #Using Twitter Python API wrapper
    #retry_count tells the API to not try again when it fails
    #originally this was unnecessary but after downloading the sample random tweets, something
    #got messed up and after implementng this it fixed itself
    api = tweepy.API(auth, retry_count=0, wait_on_rate_limit=True)
    
    # iterate through Tweepy's cursor function to gather latest tweets 
    # convert each status to an ascii string
    # add the tweet to a .txt file named after the search word
    for status in tweepy.Cursor(api.search, q).items(max_tweets):
        stringStatus = status.text.encode('ascii', 'ignore')
        tweetTxtObject.write(stringStatus)

    return filename 

# note: best to interact with user in main function then pass these variable to f(n)
def main():

    #Set Twitter authentication keys
    ckey = os.environ.get('CKEY')
    ctoken = os.environ.get('CTOKEN')
    atoken = os.environ.get('ATOKEN')
    asecret = os.environ.get('ASECRET')

    auth = OAuthHandler(ckey, ctoken)
    auth.set_access_token(atoken, asecret)
    
    q = raw_input("What word would you like to search twitter for? ").lower()
    max_tweets = int(raw_input("How many tweets would you like to search? ").lower())
    
    getStatuses(q, max_tweets, auth)

#standard boilerplate that calls the main() function
if __name__ == '__main__':
    main()












