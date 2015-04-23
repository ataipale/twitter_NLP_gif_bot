
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
import numpy as np
import re
import twokenizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF
import langdetect 
import pickle

filter_prefix_set = ('@', 'http', 'rt', 'www')

def processTweets(tweets):
    for status in tweets:
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

def processJsonData(JSON_array):

    tword_array = []
    tweets = []
    # parse each tweet to retrieve status and seperate each word
    for item in JSON_array:
        # take only status for JSON file
        status = item.get("text")
        if status:
            tweets.append(status)

    return processTweets(tweets)        

def transform_tweet(tweet):
    return transform_tweets([tweet])

def transform_tweets(tweets):
    # Read Model from File
    model = pickle.load( open( "awesome.model", "rb" ) )

    # Prepare Data for Transformation
    processed_data, feature_names, tword_array = processTweets(tweets)  
    npmatrix = np.array(processed_data.toarray())

    # Transform Data against Model
    doc_topic_test = model.transform(npmatrix)

    for title, topics in zip(tword_array, doc_topic_test):
        print("{} (top topic: {})".format(title, topics.argmax()))

# note: best to interact with user in main function then pass these variable to f(n)
def main():

    '''
    Read in $LIMIT tweets, and transform them against model that was saved to file
    '''

    limit = 200

    # convert json into array of statuses
    data = []
    n = 0
    with open('sample_tweets2.json') as data_file:
        for line in data_file:
            data.append(json.loads(line))
            n += 1
            if n == limit:
                break

    # Read Model from File
    model = pickle.load( open( "awesome.model", "rb" ) )

    # read topic words
    topic_words = pickle.load( open("awesome.topic_words_array", 'rb'))

    # Prepare Data for Transformation
    processed_data, feature_names, tword_array = processJsonData(data)  
    npmatrix = np.array(processed_data.toarray())

    # Transform Data against Model
    doc_topic_test = model.transform(npmatrix)

    n_top_words = 8

    print doc_topic_test
    print topic_words[1]
    print type(topic_words)
    for topic in topic_words:
        # print topic
        print type(topic)

        # print np.array(feature_names)[np.argsort(topic)][:-n_top_words:-1]


    for title, topic_number in zip(tword_array, doc_topic_test):
        print type(doc_topic_test)
        print("(TOPIC {}:: {} ::) {} ".format(topic_number.argmax(), topic_words[topic_number.argmax()], title) )

#standard boilerplate that calls the main() function
if __name__ == '__main__':
    main()

