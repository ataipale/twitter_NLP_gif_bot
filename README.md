# Twitter Gif Bot

This project creates a Twitter bot that responds to a bot-directed tweet with a gif that expressed the text of the tweet.

##How it works

The bot uses an uneccessarily complicated method to respond to a user's tweet. It fits the user tweet to an Latent Dirichlet Allocation model trained on a [large bank of random tweets](https://dev.twitter.com/streaming/reference/get/statuses/sample) downloaded from twitter. This fit returns an topic list of 8 topics under which the tweet falls under and then chooses three random tweets from the list and searches giphly for the tweets. This search returns a gif that is then sent back to the user. 
