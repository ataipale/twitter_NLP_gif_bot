
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

# process and clean the tweets and return a TDM of tweets/vocab and 
# vocab(feature_names)
def processTweets(tweets):
    tword_array = []
    clean_tweets = []
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
                    clean_tweets.append(tweet_split)

    print "[BEGIN] Count Vectorizing"
    count_vectorizer = CountVectorizer(min_df = 2, stop_words = 'english')
    matrix = count_vectorizer.fit_transform(tword_array)
    print "[END] Count Vectorizing"

    feature_names = np.array(count_vectorizer.get_feature_names())
    print feature_names

    return (matrix, feature_names, clean_tweets)

def processJsonData(JSON_array):
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
    processed_data, feature_names, tweets = processTweets(tweets)  
    npmatrix = np.array(processed_data.toarray())

    # Transform Data against Model
    doc_topic_test = model.transform(npmatrix)

    for title, topics in zip(tweets, doc_topic_test):
        print("{} (top topic: {})".format(title, topics.argmax()))

# note: best to interact with user in main function then pass these variable to f(n)
def main():

    '''
    Read in $LIMIT tweets, and transform them against model that was saved to file
    '''

    limit = 2000

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
    print "[BEGIN] Reading Onject"
    model_object = pickle.load(open( "awesome.object", "rb" ))
    print "[END] Reading Object"

    # topic_words is a matrix of point estimate of word distribution per topic. 
    # Shape = [n_topics, n_features]
    model = model_object.get('model')
    topic_words = model.components_
    feature_names_model = model_object.get('feature_names')
    topic_dict = model_object.get('topic_dict')

    # print "[BEGIN] Reading Feature Names"
    # feature_names_model = pickle.load( open("awesome.feature_names", "rb"))
    # print feature_names_model
    # print "[END] Reading Feature Names"

    # Prepare Data for Transformation
    print "[BEGIN] Processing Data"
    processed_data_TDM, feature_names_newtweet, tweets = processJsonData(data)  
    npmatrix = np.array(processed_data_TDM.toarray())
    print "[END] Processing Data"

    # Transform Data against Model
    # Returns:
        # doc_topic : array-like, shape (n_samples, n_topics)
        # Point estimate of the document-topic distributions
        
    # Below:
    # gives us an array of possible topics, 
    # take argmax to get the topic that matches the doc
    # doc_topic = model.doc_topic_
    # do we actually want the below at all??????? No...
    doc_topic = model.transform(npmatrix)

    n_top_words = 8
    # for topic in topic_words:
    #     # print topic
    #     # print type(topic)
    #     print np.array(feature_names_model)[np.argsort(topic)][:-n_top_words:-1]

    for title, topic_dist in zip(tweets, doc_topic):
        # topic_words = np.array(feature_names_model)[np.argsort(topic_dist)][:-n_top_words:-1]
        print("(TOPIC {} ::) {} ".format(' '.join(topic_dict[topic_dist.argmax()]), title) )

    # print doc_topic_test
    # print topic_words[1]
    # print type(topic_words)
    # for topic in topic_words:
    #     # print topic
    #     print type(topic)

    #     # print np.array(feature_names)[np.argsort(topic)][:-n_top_words:-1]

    # for title, topic_number in zip(tweets, doc_topic_test):
    #     print type(doc_topic_test)
    #     print("(TOPIC {}:: {} ::) {} ".format(topic_number.argmax(), topic_words[topic_number.argmax()], title) )

    print len(doc_topic_test)

#standard boilerplate that calls the main() function
if __name__ == '__main__':
    main()

