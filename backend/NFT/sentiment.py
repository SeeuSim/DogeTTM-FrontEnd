from . import mnemonic_query
import requests
import os
import datetime
import timedelta
import requests
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
# import sentiment as stm
import tensorflow as tf
import json
import collections
import numpy as np
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

API_key = os.environ.get('TWITTER_API_KEY')
API_Secret = os.environ.get('TWITTER_API_SECRET')
Bearer_Token = os.environ.get('TWITTER_BEARER_TOKEN')
search_url = "https://api.twitter.com/2/tweets/search/recent"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': '(test) (lang:en)',
    #'tweet_mode' : 'extended',
    'max_results': '30',
    'tweet.fields': 'created_at,lang'}
    #query_params = {'query': '(from:twitterdev -is:retweet) OR #twitterdev','tweet.fields': 'author_id'}

def getSentiment(name, params=None):
  """
  Takes in String name of token,
  Returns a tuple of float(3dp) sentiment score, and a dictionary count of pos, neu, and neg sentiments.
  """
  search_url = "https://api.twitter.com/2/tweets/search/recent"

  # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
  # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields

  query_params['query'] = name + '(lang:en)'

  def bearer_oauth(r):
      """
      Method required by bearer token authentication.
      """

      r.headers["Authorization"] = f"Bearer {Bearer_Token}"
      r.headers["User-Agent"] = "v2RecentSearchPython"
      return r

  #add &tweet_mode=extended to end of URL for full-length tweets
  def connect_to_endpoint(url, params):
      #url = url + "&tweet_mode=extended"
      response = requests.get(url, auth=bearer_oauth, params=params)
      if response.status_code != 200:
          raise Exception(response.status_code, response.text)
      return response.json()

  def analyse(tweet):
    df={}
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(tweet)["compound"]
    sentiment = np.select([sentiment_score < 0, sentiment_score == 0, sentiment_score > 0],
                            ['neg', 'neu', 'pos'])
    return sentiment, sentiment_score

  json_response = connect_to_endpoint(search_url, query_params)
  jsonString = (json.dumps(json_response, indent=4, sort_keys=True))
   #removes search_url and query_params from inside jsonString
  jsonString = jsonString.rstrip('\nendpoint')
  response = json.loads(jsonString)
  try:
    array = [x['text'] for x in response['data']]
  except:
    print("No tweet data in this time frame for " + name)
    return ["0", None]

  sentimentRatio = dict.fromkeys(['pos','neu','neg'], 0)
  avgScore = 0
  length = len(array)
  for i in range(length):
    sentiment, score = analyse(array[i])
    avgScore += score
    if sentiment == 'pos':
        sentimentRatio['pos'] += 1
    elif sentiment == 'neg':
        sentimentRatio['neg'] += 1
    else:
        sentimentRatio['neu'] += 1

  return float("{:.3f}".format(avgScore/length)), sentimentRatio


def getPastSentiment(name, time):
  """
  Input: String : Name of collection, Integer : Time in minutes
  Output: Same as getSentiment(name)
  """
  endpoint = 'https://api.twitter.com/2/tweets/search/recent'
  headers = {'authorization': f'Bearer {Bearer_Token}'}

  dtformat = '%Y-%m-%dT%H:%M:%SZ'

  def time_travel(now, mins):
      now = datetime.strptime(now, dtformat)
      back_in_time = now - timedelta(minutes=mins)
      return back_in_time.strftime(dtformat)

  now = datetime.now()
  last_week = now - timedelta(days=7)
  now = now.strftime(dtformat)

  pre = time_travel(now, time)
  query_params['start_time'] = pre
  query_params['end_time'] = now

  return getSentiment(name)

def getPastSentimentExact(name, time):
  """
  Input: String : Name of collection, Integer : Exact formatted time
  Output: A tuple of float(3dp) sentiment score, and a dictionary count of pos, neu, and neg sentiments.
  """
  endpoint = 'https://api.twitter.com/2/tweets/search/recent'
  headers = {'authorization': f'Bearer {Bearer_Token}'}
  dtformat = '%Y-%m-%dT%H:%M:%SZ'
  parsedTime = datetime.datetime.strptime(time, dtformat)
  parsedTime = parsedTime + datetime.timedelta(hours=47) #to overcome twitter API 7 days limit
  endTime = parsedTime + datetime.timedelta(hours=24)
  endTime = datetime.datetime.strftime(endTime, dtformat)
  time = datetime.datetime.strftime(parsedTime, dtformat)
  query_params['start_time'] = time
  query_params['end_time'] = endTime

  return getSentiment(name)
