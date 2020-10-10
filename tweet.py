from requests_oauthlib import OAuth1Session
import json
import os

twitter = OAuth1Session(os.environ["CONSUMER_KEY"], os.environ["CONSUMER_SECRET"], os.environ["ACCESS_TOKEN_KEY"], os.environ["ACCESS_TOKEN_SECRET"])

text = "Herokuからツイートいたしました。"
params = {"status": text}
req = twitter.post("https://api.twitter.com/1.1/statuses/update.json", params = params)