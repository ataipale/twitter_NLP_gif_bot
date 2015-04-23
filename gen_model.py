
import json

from awesome_lda import processTweets
from awesome_lda import countVectorize
from awesome_lda import getRealWords
from awesome_lda import getEnglishTweets
from awesome_lda import processJsonData
from awesome_lda import trainModel
from awesome_lda import getTopics
from awesome_lda import saveModel

n_top_words = 8
twitter_file = 'sample_tweets2.json'
model_file = 'awesome.object'

def main():

    print "file start"

    # convert json into array of statuses
    data = []
    with open(twitter_file) as data_file:
        for line in data_file:
            data.append(json.loads(line))

    print "[BEGIN] Processing"
    tweets = processJsonData(data[:1000])
    processed_data_tdm, feature_names, _ = processTweets(tweets)
    print "[END] Processing"

    model = trainModel(processed_data_tdm)
    topic_dict = getTopics(model, feature_names, n_top_words)
    saveModel(model, feature_names, topic_dict, model_file)

#standard boilerplate that calls the main() function
if __name__ == '__main__':
    main()

