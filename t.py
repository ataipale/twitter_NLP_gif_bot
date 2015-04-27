#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import tweepy
import urllib2
import argparse, logging, time, sys, os, json

import awesome_lda
import read_model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate Limit for status/mentions_timeline is 15 req / 15 min
sleep_time = 90
mentions_count = 200

GIPHY_API_KEY = 'dc6zaTOxFJmzC'

'''

Run
===

$ source config.sh && python t.py

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
GIPHY_API_KEY   = os.environ.get('GIPHY_API_KEY')
CONSUMER_KEY    = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_KEY      = os.environ.get('ACCESS_KEY')
ACCESS_SECRET   = os.environ.get('ACCESS_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def getGifUrl(q):
  gif_results = json.loads(giphyApi(q, GIPHY_API_KEY))
  logger.info("Gif Results Length: {}".format(len(gif_results["data"])))
  try:
    return gif_results["data"][0]["images"]["fixed_height"]["url"]
  except:
    return "http://media.giphy.com/media/cwTtbmUwzPqx2/giphy.gif"

def saveGifFromUrl(gif_url, filename):
  r = urllib2.urlopen(gif_url)
  f = open(filename, 'w+')
  f.write(r.read())
  f.close()

def gifFlow(q, user, status_id):
  filename = "gif/temp.gif"
  gif_url = getGifUrl(q)
  saveGifFromUrl(gif_url, filename)
  postGif(api, filename, user, status_id)
  os.remove(filename)

def giphyApi(q, api_key):
  # http://api.giphy.com/v1/gifs/search?q=funny+cat&api_key=dc6zaTOxFJmzC   
  resp = urllib2.urlopen('http://api.giphy.com/v1/gifs/search?q=' + q + '&api_key=' + GIPHY_API_KEY).read()
  return resp

def postGif(api, filename, user, status_id):
  status = "A gif for you dear @" + user
  return api.update_with_media(filename=filename, status=status, in_reply_to_status_id=status_id)

def onMentions(since_id):

    logger.info('Start fetching mentions')

    mentions = None

    if since_id is None:
        mentions = api.mentions_timeline(count=mentions_count)
    else:
        mentions = api.mentions_timeline(count=mentions_count, since_id=since_id)

    logger.info('Mention Count: %i', len(mentions))

    for mention in reversed(mentions):
        user = mention.user.screen_name
        text = mention.text
        since_id = mention.id
        
        # handwavey
        topic_query_arr = read_model.tweet_to_topic(text, 3)
        topic_query_str = "-".join(topic_query_arr)
        # topic = "gorilla"

        gifFlow(topic_query_str, user, since_id)

    return since_id

def postGifExample():
  q = "dolphin"
  user = "djdrozdov"
  status_id = "588398082116739072"
  gifFlow(q, user, status_id)

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument('since_id', nargs='?')
  args = parser.parse_args()

  since_id = args.since_id

  while(1):
    since_id = onMentions(since_id)
    time.sleep(sleep_time)

