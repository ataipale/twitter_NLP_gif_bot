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
import re
import twokenizer
from sklearn.feature_extraction.text import TfidfVectorizer

common_words = open('google-10000-english.txt', 'r').read().splitlines()
common_words_set = set(common_words[0:200])

filter_prefix_set = ('@', 'http', 'rt', 'www')

def processJsonData():

    # convert json into array of statuses
    data = []
    with open('sample_tweets2.json') as data_file:
        for line in data_file:
            data.append(json.loads(line))

    tword_array = []
    # parse each tweet to retrieve status and seperate each word
    for item in data[0:24000]:
        status = item.get("text")
        # write the statuses as a string to a .txt doc
        filename = "parsed_sample_tweets.txt"
        randomTweetObject = open(filename, 'w')
        if status:
            tweet_split = status.encode('ascii', 'ignore').lower()
            tokenized = twokenizer.tokenize(tweet_split)
            # print tokenized
            no_stopwords_tweet = [word for word in tokenized if word not in common_words_set]
            just_real_words = [re.sub(r'[^\w\s]','', word) for word 
                                        in no_stopwords_tweet 
                                        if not word.startswith(filter_prefix_set)
                                        and len(word) >= 4
                                    ]
            if just_real_words:
                tword_array.append(" ".join(just_real_words))
    print len(tword_array)
    return tword_array

    # print tword_array[0:200]

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
def create_TDM(tword_array):
    # doc2 = "testdoc2.txt"
    # Initialize class to create term-document matrix
    tdm = textmining.TermDocumentMatrix()
    # Add the documents, documents must come as strings
    for tweet in tword_array:
        tdm.add_doc(tweet)
        
    # Rows returns a generator. Note that setting cutoff=1 means
    # that words which appear in 1 or more documents will be included in
    # the output (i.e. every word will appear in the output). The default
    # for cutoff is 2, since we usually aren't interested in words which
    # appear in a single document. For this example we want to see all
    # words however, hence cutoff=1.
    matrixGenerator = tdm.rows(cutoff=1)
    matrix_vocab = matrixGenerator.next()
    matrix_array = []
    # matrix_topics = ["girl", "random"]
    for row in matrixGenerator:
        matrix_array.append(row)

    matrix = np.array(matrix_array)

    print matrix.shape
   
    # Instead of writing out the matrix you can also access its rows directly.
    # Let's print them to the screen.
    # for row in tdm.rows(cutoff=1):
    #     print row
    # print tdm

    model = lda.LDA(n_topics=40, n_iter=500, random_state=1)
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
    
    # q = raw_input("What word would you like to search twitter for? ").lower()
    # max_tweets = int(raw_input("How many tweets would you like to search? ").lower())
    
    create_TDM(processJsonData())
    # getStatuses(q, max_tweets, auth)
    # processJsonData()

#standard boilerplate that calls the main() function
if __name__ == '__main__':
    main()












