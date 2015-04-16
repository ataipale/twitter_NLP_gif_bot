
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
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF
import langdetect 

import pickle

filter_prefix_set = ('@', 'http', 'rt', 'www')

def processJsonData(JSON_array):

    tword_array = []
    tweets = []
    # parse each tweet to retrieve status and seperate each word
    for item in JSON_array:
        # take only status for JSON file
        status = item.get("text")
        if status:
            # ignore non-ascii characters, make all lowercase letters
            tweet_split = status.encode('ascii', 'ignore').lower()
            # get rid of useless characters in tweets, and makes words from string
            if tweet_split:
                # ignore non-English tweets
                # print tweet_split
                try:
                    lang = langdetect.detect(tweet_split)
                except langdetect.lang_detect_exception.LangDetectException:
                    continue
                if  lang == 'en':
                    # print "entered loop!"
                    tokenized = twokenizer.tokenize(tweet_split)
                    # get rid of stopwords
                    # no_stopwords_tweet = [word for word in tokenized if word not in common_words_set]
                    # get rid of punctuation and internet terms
                    just_real_words = [re.sub(r'[^\w\s]','', word) for word 
                                                in tokenized 
                                                if not word.startswith(filter_prefix_set)
                                                
                                            ]
                    if just_real_words:
                        tword_array.append(" ".join(just_real_words))
                        tweets.append(tweet_split)

    count_vectorizer = CountVectorizer(min_df = 2, stop_words = 'english')
    matrix = count_vectorizer.fit_transform(tword_array)
    print matrix[:10]

    feature_names = np.array(count_vectorizer.get_feature_names())
    print feature_names
    # print matrix.shape

    return (matrix, feature_names, tweets)

def log(str):
    print "\n@@@@@@@@@@@\n"
    print 
    print "\n@@@@@@@@@@@\n"

# note: best to interact with user in main function then pass these variable to f(n)
def main():

    # convert json into array of statuses
    data = []
    with open('sample_tweets2.json') as data_file:
        for line in data_file:
            data.append(json.loads(line))

    testing_size = 20

    processed_data, feature_names, tword_array = processJsonData(data[:1000])  

    npmatrix = np.array(processed_data.toarray())

    model = pickle.load( open( "awesome.model", "rb" ) )
    model.transform(npmatrix[:testing_size])

    doc_topic_test = model.transform(npmatrix[:testing_size])

    # print doc_topic_test

    for title, topics in zip(tword_array[:10], doc_topic_test):
        print("{} (top topic: {})".format(title, topics.argmax()))

    sys.exit(1)

#standard boilerplate that calls the main() function
if __name__ == '__main__':
    main()

