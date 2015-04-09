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
import numpy as np

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

# Term Document Matrix maker only takes strings, so converting doc to string
def docToString(textDoc):
    docString = ''
    with open(textDoc) as txt_file:
        for line in txt_file:
            if line:
                line.encode('ascii', 'ignore')
                docString = docString + line
    return docString
            
# create Term Document Matrix for LDA analysis
def create_TDM(searchFile):
    doc1 = "sample_tweets2.txt"
    doc2 = searchFile
    # doc1 = "testdoc1.txt"
    # doc2 = "testdoc2.txt"
    # Initialize class to create term-document matrix
    tdm = textmining.TermDocumentMatrix()
    # Add the documents, documents must come as strings
    tdm.add_doc(docToString(doc1))
    tdm.add_doc(docToString(doc2))
    # Rows returns a generator. Note that setting cutoff=1 means
    # that words which appear in 1 or more documents will be included in
    # the output (i.e. every word will appear in the output). The default
    # for cutoff is 2, since we usually aren't interested in words which
    # appear in a single document. For this example we want to see all
    # words however, hence cutoff=1.
    matrixGenerator = tdm.rows(cutoff=1)
    matrix_vocab = matrixGenerator.next()
    # matrix_topics = ["girl", "random"]
    matrix = np.array([matrixGenerator.next(), matrixGenerator.next()])
    print type(matrix)
    print matrix.shape
    # Instead of writing out the matrix you can also access its rows directly.
    # Let's print them to the screen.
    # for row in tdm.rows(cutoff=1):
    #     print row
    # print tdm

    model = lda.LDA(n_topics=10, n_iter=500, random_state=1)
    model.fit(matrix)
    topic_word = model.topic_word_  # model.components_ also works
    n_top_words = 8
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(matrix_vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))

    # for n in range(10):
    # topic_most_pr = doc_topic[n].argmax()
    # print("doc: {} topic: {}\n{}...".format(n,
    #                                         topic_most_pr,
    #                                         titles[n][:50]))
    


# write about rate limit data
def getRateLimit():
    with open('rate_limit.json', 'w') as outfile:
        json.dump(api.rate_limit_status(), outfile, sort_keys=True, indent=4)


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
    
    create_TDM(getStatuses(q, max_tweets, auth))
    # getStatuses(q, max_tweets, auth)

#standard boilerplate that calls the main() function
if __name__ == '__main__':
    main()












