
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

def processJsonData(JSON_array):

    tword_array = []
    # xxx wait.... why are we making tweets?
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

    # use Sklearn's kit to fit and transform the array of just real words from the 
    # tweets and make TDM
    count_vectorizer = CountVectorizer(min_df = 2, stop_words = 'english')
    TDM = count_vectorizer.fit_transform(tword_array)
    print TDM[:10]

    feature_names = np.array(count_vectorizer.get_feature_names())
    print feature_names
    # print matrix.shape

    return (TDM, feature_names, tweets)

def log(str):
    print "\n@@@@@@@@@@@\n"
    print 
    print "\n@@@@@@@@@@@\n"


def main():

    print "file start"

    # convert json into array of statuses
    data = []
    with open('sample_tweets2.json') as data_file:
        for line in data_file:
            data.append(json.loads(line))

    # for cutting off beginning portion of data for testing purposes
    testing_size = 20

    # to avoid looking at the entire data set when testing
    test_max = 1000

    print "before data"

    processed_data_TDM, feature_names, tweets = processJsonData(data[testing_size:test_max])  

    npmatrix = np.array(processed_data_TDM.toarray())

    model = lda.LDA(n_topics=40, n_iter=50, random_state=1)
    model.fit(npmatrix)

    # topic_word is a matrix of point estimate of word distribution per topic. 
    # Shape = [n_topics, n_features]
    topic_word = model.components_  
    n_top_words = 8
    # topic_words_array = []
    for i, word_dist in enumerate(topic_word):
        print "Here are feature_names:"
        # print type([np.argsort(word_dist)])
        # print np.array(feature_names)
        # Below: For each feature, sort the word distribution and give me 
        # the 8 last words (largest word dist??)
        topic_words = np.array(feature_names)[np.argsort(word_dist)][:-n_top_words:-1]
        # topic_words_array[i] = topic_list
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))

    pickle.dump( model , open( "awesome.model", "wb" ) )

    log(model.components_)

#standard boilerplate that calls the main() function
if __name__ == '__main__':
    main()

