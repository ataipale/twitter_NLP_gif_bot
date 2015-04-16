#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import tweepy, time, sys, os
import logging
import urllib2

argfile = str(sys.argv[1])
since_id = None if len(sys.argv) < 3 else str(sys.argv[2])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sleep_time = 5
mentions_count = 200

GIPHY_API_KEY = 'dc6zaTOxFJmzC'

'''

Steps
=====

1. Periodically check mentions since since_id
2. For each new mention, run against our model to get a topic
  3. Use the assigned topic as input to a giphy_api to get a gif_url
  4. Download image from gif_url
  5. Upload the gif_url to Twitter and get media_id
  6. Respond to mention with attached media_id

'''
 
#enter the corresponding information from your Twitter application:
CONSUMER_KEY    = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_KEY      = os.environ.get('ACCESS_KEY')
ACCESS_SECRET   = os.environ.get('ACCESS_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def logstr(ltype, data):
  return '[' + str(ltype) + ';;;' + str(data) + ']'

def giphyApi(q, api_key):
  # http://api.giphy.com/v1/gifs/search?q=funny+cat&api_key=dc6zaTOxFJmzC   
  resp = urllib2.urlopen('http://api.giphy.com/v1/gifs/search?q' + q + '&api_key=' + GIPHY_API_KEY).read()
  print resp

def onMentions(since_id):

    logger.info('Start fetching mentions')

    mentions = None

    if since_id is None:
        mentions = api.mentions_timeline(count=mentions_count)
    else:
        mentions = api.mentions_timeline(count=mentions_count, since_id=since_id)

    logger.info('Mention Count: %i', len(mentions))

    for mention in reversed(mentions):
    #     # respond to mention

    #     user = mention.user.screen_name
    #     text = mention.text # there's no @
    #     topic = model.transform(text)
    #     img_url = giphyApi(topic.text, GIPHY_API_KEY)
    #
    #     msg = '@' + user + ' ' + img_url
    #     
    #     print 
        since_id = mention.id
        logger.info(logstr('mention', since_id))
    #     api.update_status(line)
    #     time.sleep(5)

    return since_id

if __name__ == "__main__":
    while(1):
        since_id = onMentions(since_id)
        time.sleep(sleep_time)
