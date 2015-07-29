# Twitter Gif Bot

This project creates a Twitter bot that uses machine learning algorithms to turn your tweets into Gifs!

##How it works

The bot uses an uneccessarily complicated method to respond to a user's tweet. It fits the user tweet to an Latent Dirichlet Allocation model trained on a [large bank of random tweets](https://dev.twitter.com/streaming/reference/get/statuses/sample) downloaded from twitter. This fit returns an topic list of topics under which the tweet falls under and then chooses three random tweets from the list and searches giphly for the tweets. This search returns a gif that is then tweeted back to the user. 

##Run
You will need your own twitter and Giphy API authentication keys stored in config.sh file.
```
$ source config.sh && python t.py
```
Everytime the program is run it will send tweets at all tweets at the bot since it was last run. You can specify a Tweet ID when calling t.py to only respond to tweets since a certain ID. 
