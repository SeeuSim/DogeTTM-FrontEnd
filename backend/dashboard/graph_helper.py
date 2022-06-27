#Copy pasting over from notebook once I'm done
import os

import dotenv
import matplotlib.pyplot as plt
import pandas as pd

from . import price_helper

dotenv.load_dotenv("../frontend/.env")
"""Rarify Config"""
RARIFY_API_KEY:str = os.environ.get('RARIFY_API_KEY')

"""Twitter Config"""
API_key = os.environ.get('TWITTER_API_KEY')
API_Secret = os.environ.get('TWITTER_API_SECRET')
Bearer_Token = os.environ.get('TWITTER_BEARER_TOKEN')

def graphPastSentiment(name, days):
  search_url = "https://api.twitter.com/2/tweets/search/recent"

  daysArr = []
  priceArr = []
  sentimentArr = []
  for i in range(days):
      daysArr.append(i+1) #X-axis: Days array in a week
      currSentiments = price_helper.getPastSentiment(name, (7-i+1) * 1440) #With day 7 as current day, start from day 0,
                                                              #so first day will be (7-1+1) * 1440 minutes in the past
      sentimentArr.append(currSentiments[0])                    #currSentiments return a tuple of (sentimentScore, sentimentRatio),
                                                              #we want sentimentScore as Y-Axis here
  plt.title('Sentiment of ' + name + ' over ' + str(days) + ' days')
  plt.xlabel('Days')
  plt.ylabel('Sentiment Score')
  plt.plot(daysArr, sentimentArr)

