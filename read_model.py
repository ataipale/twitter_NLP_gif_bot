import lda
import json
import awesome_lda

model_file = "awesome.object" 

# note: best to interact with user in main function then pass these variable to f(n)
def main():

    '''
    Read in $LIMIT tweets, and transform them against model that was saved to file
    '''

    limit = 100

    # convert json into array of statuses
    data = []
    with open('sample_tweets2.json') as data_file:
        for line in data_file:
            data.append(json.loads(line))

    # Read Model from File
    model, _, topic_dict = awesome_lda.loadModel(model_file)
    
    tweets = awesome_lda.processJsonData(data[:limit])

    # Transform Data against Model
    # Returns:
        # doc_topic : array-like, shape (n_samples, n_topics)
        # Point estimate of the document-topic distributions
    doc_topic, real_tweets = awesome_lda.transform_tweets(model, tweets)

    awesome_lda.printTransformedTweets(real_tweets, doc_topic, topic_dict)

if __name__ == '__main__':
    main()

