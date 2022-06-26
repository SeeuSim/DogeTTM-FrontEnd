#Retrieve all tokens in a collection
import requests
from decimal import Decimal
import matplotlib.pyplot as plt
import pandas as pd
from operator import itemgetter
from datetime import datetime, timedelta
import os
import json
#import flair
import collections

RARIFY_API_KEY = '1959b00b-435b-4c27-a1b7-66168414d0dc'


def format_price(price:str, currency:str):
  """Prices are in format of 18 decimals"""
  # Returns the price in a readable format, given the 18 decimal raw price

  return f"{(Decimal(price).normalize() * (Decimal('10')**Decimal('-18'))).__str__()} {currency}"

"""Retrieves the price history for a collection in 24h, 7d, 30d, all_time"""
# 24h: 24 entries 1h apart
# 7d: 7 entries 1d apart
# 30d: 30 entries 1d apart

def get_price_history(address, coin, time_period):
  endpoint = f"https://api.rarify.tech/data/contracts/{coin}:{address[2:]}/insights/{time_period}"
  headers = {
      "Authorization": f'Bearer {RARIFY_API_KEY}'
  }
  response = requests.get(endpoint, headers=headers).json()
  if 'errors' in response:
    return response
  return response['included'][-1]['attributes']['history']

  

# get_price_history("0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB", "ethereum", "24h")
#print([(format_price(x['avg_price'], "ETH"), x['time']) for x in get_price_history("0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB", "ethereum", "30d")])


"""Get trade history for a token"""
# To get metadata, remove the insights from the endpoint
def token_trades(address:str, coin:str, id:int, time_period:str) -> dict or list:
  if len(address) != 42: return ["Error: invalid address"]
  raw_id = hex(id)
  if len(raw_id) % 2 == 0:
    raw_id = raw_id[2:]
  else:
    raw_id = raw_id.replace('x', '')

  endpoint = f"https://api.rarify.tech/data/tokens/{coin}:{address[2:]}:{raw_id}/insights/{time_period}"
  headers = {
      "Authorization": f'Bearer {RARIFY_API_KEY}'
  }
  response = requests.get(endpoint, headers=headers).json()
  if 'included' not in response:
    return response
  return response['included'][1]['attributes']['history']

#print(token_trades("0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D", "ethereum", 2087, "365d"))


"Find collections, given the name as a string"

"""To Find specific tokens in the collection, given ID and collection"""
"""
 1st: find_collections(name)
 2nd: select collection and save contract ID as 'id_from_contract'
 3rd: search w the following params, similar to find_collections

 params = {
   'filter[contract]": f'{id_from_contract}',
   'filter[name]": f'{token_id}'
   'include': 'metadata'
 }
"""

def find_collections(name:str) -> dict or list:
    endpoint = 'https://api.rarify.tech/data/contracts'
    headers = {
        "Authorization": f'Bearer {RARIFY_API_KEY}'
    }
    params = {
        'filter[name]': name
        #'filter[contract]": f'{id_from_contract}',    
        #'filter[name]": f'{token_id}'
        #'include': 'metadata'
    }
    response = requests.get(endpoint, headers=headers, params=params).json()

    if 'errors' in response:
        return response
    return response['data']


def get_trending(limit:int, period:str) -> dict or list:
  endpoint = 'https://api.rarify.tech/data/contracts'
  headers = {
      "Authorization": f'Bearer {RARIFY_API_KEY}'
  }
  periods = {'24h', '3d', '7d', '30d', '90d'}
  if period not in periods:
    raise ValueError("Wrong time period selected. Choose from '24h', '3d', '7d', '30d', or '90d'")
  if limit < 5:
    limit = 5

  params = {
      'insights_trends.period': period,
      # 'include': 'insights',
      'include': 'insights_trends',
      'sort': '-insights_trends.volume_change_percent',
      # 'sort': '-insights.volume',
      # 'sort': '-insights.min_price',
      'page[limit]': limit
  }
  response = requests.get(endpoint, headers=headers, params=params).json()
  #return response;
  #return [x for x in zip(response['data'], response['included'])]

  tokens = response['data']
  stats = response['included']
  
  out = []
  
  for token, stat in zip(tokens, stats):
    nm = ""
    if 'name' in token['attributes']:
      nm = token['attributes']['name']
    out.append({
        "address": f"0x{token['attributes']['address']}",
        "name": nm,
        "tokens": token['attributes']['tokens'],
        "unique_owners": token['attributes']['unique_owners'],
        "volume_change": format_price(stat['attributes']['volume_change'],stat['attributes']['payment_asset']['code']),
        "percent_change": stat['attributes']['volume_change_percent']
    })

  return out

def get_top(param:str, limit:int) -> dict or list:
  if param not in {"min_price", 'max_price', 'volume'}:
    raise ValueError("wrong param. Choose from 'min_price', 'max_price', or 'volume'")
  if limit < 5:
    limit = 5
  endpoint = 'https://api.rarify.tech/data/contracts'
  headers = {
      "Authorization": f'Bearer {RARIFY_API_KEY}'
  }

  params = {
      'include': 'insights',
      'sort': f'-insights.{param}',
      'page[limit]': limit
  }

  response = requests.get(endpoint, headers=headers, params=params).json()
  return response
  # return  [x for x in zip(response['data'], response['included'])]

def plotTop():
    temp = get_trending(10, '3d')
    tokenName = []
    tokenPChange = []
    tokenVChange = []
    topRising = []
    for i in range(len(temp)):
        tokenName.append(temp[i]['name'])
        tokenPChange.append(temp[i]['percent_change'])
        tokenVChange.append(temp[i]['volume_change'])
        topRising.append([temp[i]['name'], temp[i]['percent_change'], temp[i]['volume_change']])


    fig = plt.figure()
    dataArr = sorted(topRising,key=itemgetter(1))
    plt.bar(tokenName, tokenPChange)
    #plt.bar(get_trending(10, '3d'), 10)



#These are the code that will go into views.py 

#Sentiment Code
def getSentiment():
    API_key = "dSnZQuCPMVQfCXGhhgWJ6qs8s"
    API_Secret = "uwgDp27NZ2sEsHfV7oGY95Dy0di38mhQDs9FjzJSfM6n2ejfSr"
    Bearer_Token = "AAAAAAAAAAAAAAAAAAAAAAgQcgEAAAAAtvIEDNCuREcrZhCu3j9F%2FmhXz00%3DQdawgUlRgpvd2eMyeAug3tPY89yuWvjqVV7NWXlvQX00CJIauI"
    search_url = "https://api.twitter.com/2/tweets/search/recent"

    # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
    # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
    query_params = {'query': '(luna) (lang:en)',
        #'tweet_mode' : 'extended',
        'max_results': '20',
        'tweet.fields': 'created_at,lang'}
    # query_params = {'query': '(from:twitterdev -is:retweet) OR #twitterdev','tweet.fields': 'author_id'}


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
        #print(response.status_code)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()

    def analyse(tweet):
        sentiment_model = flair.models.TextClassifier.load('en-sentiment')
        sentence = flair.data.Sentence(tweet)
        sentiment_model.predict(sentence)
        #print(tweet)
        #print(sentence.labels[0].value)
        #print(sentence.labels[0].score)
        return sentence.labels[0].value, sentence.labels[0].score

    json_response = connect_to_endpoint(search_url, query_params)
    jsonString = (json.dumps(json_response, indent=4, sort_keys=True))
    #removes search_url and query_params from inside jsonString
    jsonString = jsonString.rstrip('\nendpoint') 
    response = json.loads(jsonString)
    array = [x['text'] for x in response['data']]


    sentimentMap = {'POSITIVE':0, 'NEGATIVE':0}
    avgScore = 0
    length = len(array)
    for i in range(length):
        sentiment, score = analyse(array[i])
        #if-else needed because to convert score to negative 
        sentimentMap[sentiment] += 1 
        if sentiment == 'POSITIVE':
            avgScore += score
        else:
            avgScore -= score    
    return avgScore/length, sentimentMap
    #print(analyse(array[0]))


def viewIndividualNFTData(address):
    if (len(address)!= 40): #if input in the form of collection name, not address
        name = find_collections(address) #return address of collection
    return token_trades(name)
    


