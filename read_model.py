import lda
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

    '''
    Process and clean the tweets and return a TDM of tweets/vocab and 
    vocab(feature_names)
    '''

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

    '''
    Transforms Incoming tweet data and returns the tweet and topic
    '''
    # Read Model from File
    model = pickle.load( open( "awesome.object", "rb" ))

    # Prepare Data for Transformation
    processed_data_TDM, feature_names_newtweet, new_tweets = processJsonData(tweets)  
    npmatrix = np.array(processed_data_TDM.toarray())

    # Get Parts of Object Dictionary
    model = model_object.get('model')
    feature_names_model = model_object.get('feature_names')
    topic_dict = model_object.get('topic_dict')

    # topic_words is a matrix of point estimate of topic distribution per document 
    topic_words = model.components_

    # Transform Data against Model
    doc_topic = model.transform(npmatrix)

    tweet_and_topic = []
    for title, topic_dist in zip(tweets, doc_topic):
        tweet_and_topic.append(topic_dict[topic_dist.argmax()], title) 

    return tweet_and_topic

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

    model = model_object.get('model')
    feature_names_model = model_object.get('feature_names')
    topic_dict = model_object.get('topic_dict')

    # topic_words is a matrix of point estimate of word distribution per topic. 
        # Shape = [n_topics, n_features]
    topic_words = model.components_

    # Prepare Data for Transformation
    print "[BEGIN] Processing Data"
    processed_data_TDM, feature_names_newtweet, tweets = processJsonData(data)  
    npmatrix = np.array(processed_data_TDM.toarray())
    print "[END] Processing Data"

    # Transform Data against Model
    # Returns:
        # doc_topic : array-like, shape (n_samples, n_topics)
        # Point estimate of the document-topic distributions
    doc_topic = model.transform(npmatrix)

    for title, topic_dist in zip(tweets, doc_topic):
        print("(TOPIC {} ::) {} ".format(' '.join(topic_dict[topic_dist.argmax()]), title) )

if __name__ == '__main__':
    main()

