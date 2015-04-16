
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

    print "file start"

    # convert json into array of statuses
    data = []
    with open('sample_tweets2.json') as data_file:
        for line in data_file:
            data.append(json.loads(line))

    testing_size = 20

    print "before data"

    # training_matrix, feature_names = processJsonData(data[testing_size:1000])
    # model = create_TDM(training_matrix, feature_names)

    # testing_data, feature_names_2 = processJsonData(data[:testing_size])
    # matchNewTweet(model, testing_data, feature_names_2)  

    # print len(data)
    # sys.exit(1)

    processed_data, feature_names, tword_array = processJsonData(data[testing_size:1000])  

    print "\n@@@@@@@@@@@\n"
    print type(processed_data)
    print "\n@@@@@@@@@@@\n"

    npmatrix = np.array(processed_data.toarray())

    print type(npmatrix)

    model = lda.LDA(n_topics=40, n_iter=50, random_state=1)
    model.fit(npmatrix[testing_size:])

    pickle.dump( model , open( "awesome.model", "wb" ) )

    log(model.components_)

    pickle.dump( model.components_ , open( "awesome.components_", "wb" ) )

    log(model.alpha)

    pickle.dump( model.alpha , open( "awesome.alpha", "wb" ) )

#standard boilerplate that calls the main() function
if __name__ == '__main__':
    main()

