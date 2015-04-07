from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import Cursor
import sys
import os
import tweepy
import lda
import operator


#Set Twitter authentication keys
ckey = os.environ.get('CKEY')
ctoken = os.environ.get('CTOKEN')
atoken = os.environ.get('ATOKEN')
asecret = os.environ.get('ASECRET')

auth = OAuthHandler(ckey, ctoken)
auth.set_access_token(atoken, asecret)

#Using Twitter Python API wrapper
api = tweepy.API(auth)

q = raw_input("What word would you like to search twitter for? ").lower()
max_tweets = 40

filename = q + '.txt'
tweetTxtObject = open(filename, 'w')

#initiate dictionary to store counts of words 
wordCount = {}

# iterate through Tweepy's cursor function to gather latest tweets 
# convert each status to an ascii string
# add the tweet to a .txt file named after the search word
# split each statues based on white space
# increase value counter by 1 everytime we see the word
for status in tweepy.Cursor(api.search, q).items(max_tweets):
    stringStatus = status.text.encode('ascii', 'ignore')
    tweetTxtObject.write(stringStatus)
    splitWords = stringStatus.split()
    for word in splitWords:
        word = word.lower()
        wordCount[word] = int(wordCount.get(word, 0)) + 1


#make a list of the top 100 most common words
commonWords = open('google-10000-english.txt', 'rb').read().splitlines()

print "HERE ARE THE TOP TEN unimportant WORDS for %s:" % (q)
sortedList = sorted(wordCount.items(), key=lambda x: x[1], reverse=True)
print sortedList[0:9]
importantWords = [[]]
for word in sortedList:
    if word[0] not in commonWords[0:199]:
        if word[0] != q and word[0] != "rt":
            importantWords.append([word[0], word[1]])
print "HERE ARE THE TOP TEN Important WORDS for %s:" % (q)
print importantWords[0:9]

print "adding changes to practice with git, moarrrr changes. changes to LDA branch"
print "adding changes to merged branch"

















