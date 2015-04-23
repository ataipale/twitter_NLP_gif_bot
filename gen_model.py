
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

# process and clean the tweets and return a TDM of tweets/vocab and vocab(feature_names)
def processJsonData(JSON_array):

    tword_array = []
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

    # use Sklearn's kit to fit and transform the array of just real words from the 
    # tweets and make TDM
    count_vectorizer = CountVectorizer(min_df = 2, stop_words = 'english')
    TDM = count_vectorizer.fit_transform(tword_array)
    print TDM[:10]

    feature_names = np.array(count_vectorizer.get_feature_names())
    print feature_names
    # print matrix.shape

    return (TDM, feature_names)

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

    print "[BEGIN] Processing"
    processed_data_TDM, feature_names = processJsonData(data)  
    print "[END] Processing"

    npmatrix = np.array(processed_data_TDM.toarray())

    model = lda.LDA(n_topics=40, n_iter=50, random_state=1)
    model.fit(npmatrix)

    # topic_word is a matrix of point estimate of word distribution per topic. 
    # Shape = [n_topics, n_features]
    topic_word = model.components_  
    n_top_words = 8
    topic_dict = []
    for i, word_dist in enumerate(topic_word):
        print "Here are feature_names:"
        # Below: For each feature, sort the vocab based on word distribution 
        # and give me the 8 most relatively important words in each doc
        topic_words = np.array(feature_names)[np.argsort(word_dist)][:-n_top_words:-1]
        topic_dict.append(topic_words) 
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))

    pickle_dict = dict(model = model, feature_names = feature_names, topic_dict = topic_dict)
    pickle.dump( pickle_dict, open("awesome.object", "wb"))

    # log(model.components_)

    # pickle.dump( feature_names, open("awesome.feature_names", "wb") )

    # log(model.components_)

#standard boilerplate that calls the main() function
if __name__ == '__main__':
    main()

