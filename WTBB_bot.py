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
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF
import langdetect 

# common_words = open('google-10000-english.txt', 'r').read().splitlines()
# common_words_set = set(common_words[0:75])
# print common_words_set
# q = raw_input("Continue?? ").lower()

filter_prefix_set = ('@', 'http', 'rt', 'www')

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

    count_vectorizer = CountVectorizer(min_df = 2, stop_words = 'english')
    matrix = count_vectorizer.fit_transform(tword_array)
    feature_names = np.array(count_vectorizer.get_feature_names())
    print feature_names
    print matrix.shape


    return (matrix, feature_names)

    # print tword_array[0:200]
            
# create Term Document Matrix for LDA analysis
def create_TDM(matrix, feature_names):

    # print matrix
    print type(matrix)
    print matrix.shape
   
    model = lda.LDA(n_topics=40, n_iter=50, random_state=1)
    model.fit(matrix)
    print "model fit"
    topic_word = model.topic_word_  # model.components_ also works
    n_top_words = 8
    for i, topic_dist in enumerate(topic_word):
        topic_words = (feature_names)[np.argsort(topic_dist)][:-n_top_words:-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))

    # for n in range(10):
    # topic_most_pr = doc_topic[n].argmax()
    # print("doc: {} topic: {}\n{}...".format(n,
    #                                         topic_most_pr,
    #                                         titles[n][:50]))
    return model

def matchNewTweet(model, testing_data):

    found_doc = model.transform(testing_data)
    print "found_doc_shape:" + found_doc.shape
    print "transformed!!"
    for title, topics in enumerate(found_doc):
        print "entered loop!"
        print("{} (top topic: {})".format(title, topics.argmax()))


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

    # convert json into array of statuses
    data = []
    with open('sample_tweets2.json') as data_file:
        for line in data_file:
            data.append(json.loads(line))

    testing_size = 20

    # training_matrix, feature_names = processJsonData(data[testing_size:1000])
    # model = create_TDM(training_matrix, feature_names)

    # testing_data, feature_names_2 = processJsonData(data[:testing_size])
    # matchNewTweet(model, testing_data, feature_names_2)  

    processed_data, feature_names = processJsonData(data[:1000])  
    print processed_data.shape
    print processed_data[:testing_size]
    print feature_names
    model = create_TDM(processed_data[testing_size:], feature_names)
    matchNewTweet(model, processed_data[:testing_size])  
    
    # processJsonData()

#standard boilerplate that calls the main() function
if __name__ == '__main__':
    main()












