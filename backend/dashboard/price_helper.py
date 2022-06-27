import json
import os
from datetime import datetime, timedelta
from decimal import Decimal
from operator import itemgetter
from urllib import response

import dotenv
import flair
import matplotlib.pyplot as plt
import pandas as pd
import requests
from numpy import add

# import collections


dotenv.load_dotenv("../frontend/.env")
RARIFY_API_KEY:str = os.environ.get('RARIFY_API_KEY')

RARIFY_header = {
      "Authorization": f'Bearer {RARIFY_API_KEY}'
}


def format_price(price:str, currency:str):
  """Prices are in format of 18 decimals"""
  # Returns the price in a readable format, given the 18 decimal raw price
  return f"{(Decimal(price).normalize() * (Decimal('10')**Decimal('-18'))).__str__().format('.f')} {currency}"


def format_id(tokenID:int) -> str:
  hexID = hex(tokenID)
  if len(hexID) % 2 == 0:
    return hexID[2:]
  return hexID.replace('x', '')


def token_trades(address:str, coin:str, id:int, time_period:str) -> dict or list:
  """Get trade history for a token"""
# To get metadata, remove the insights from the endpoint
  if len(address) != 42: return ["Error: invalid address"]
  raw_id = hex(id)
  if len(raw_id) % 2 == 0:
    raw_id = raw_id[2:]
  else:
    raw_id = raw_id.replace('x', '')

  endpoint = f"https://api.rarify.tech/data/tokens/{coin}:{address[2:]}:{raw_id}/insights/{time_period}"

  response = requests.get(endpoint, headers=RARIFY_header).json()
  if 'included' not in response:
    return response
  return response['included'][1]['attributes']['history']


def find_collections(name:str) -> dict or list:
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
  endpoint = 'https://api.rarify.tech/data/contracts'

  params = {
      'filter[name]': name
      #'filter[contract]": f'{id_from_contract}',
      #'filter[name]": f'{token_id}'
      #'include': 'metadata'
  }
  response = requests.get(endpoint, headers=RARIFY_header, params=params).json()

  if 'errors' in response:
      return response
  return response['data']


def get_trending(limit:int, period:str) -> dict:
  """periods are '24h', '3d', '7d', '30d', or '90d'"""
  endpoint = 'https://api.rarify.tech/data/contracts'

  params = {
      'insights_trends.period': period,
      'include': 'insights_trends',
      'sort': '-insights_trends.volume_change_percent',
      'page[limit]': limit,
      'filter[has_metadata]': "true"
  }
  response = requests.get(endpoint, headers=RARIFY_header, params=params).json()

  tokens = response['data']
  stats = response['included']
  out = []

  for token, stat in zip(tokens, stats):
    tokens = token['attributes']['tokens']
    id = token['id']

    nm = ""
    if 'name' in token['attributes']:
      nm = token['attributes']['name']
    out.append({
        'id': id,
        "address": f"0x{token['attributes']['address']}",
        "name": nm,
        "tokens": tokens,
        "unique_owners": token['attributes']['unique_owners'],
        "volume_change": format_price(stat['attributes']['volume_change'],stat['attributes']['payment_asset']['code']),
        "percent_change": stat['attributes']['volume_change_percent']
    })

  return {'data':sorted(out, key=lambda x: Decimal(x['percent_change']), reverse=True)}


def get_top(param:str, limit:int) -> dict:
  """Gets the top ranking collections by search parameter.

  Parameters
  ----------
  param : str
      The ranking parameter to search by. Options: 'min_price', 'max_price', 'volume'

  limit : int
      The positive number of entries to return.
  """

  endpoint = 'https://api.rarify.tech/data/contracts'

  params = {
      'include': 'insights',
      'sort': f'-insights.{param}',
      'page[limit]': limit,
      'filter[has_metadata]': "true"
  }
  response = requests.get(endpoint, headers=RARIFY_header, params=params).json()
  tokens = response['data']
  stats = response['included']
  out = []
  for token, stat in zip(tokens, stats):
    tokens = token['attributes']['tokens']
    id = token['id']
    nm = ""
    if 'name' in token['attributes']:
      nm = token['attributes']['name']
    out.append({
        'id': id,
        "address": f"0x{token['attributes']['address']}",
        "name": nm,
        "tokens": tokens,
        "avg_price": format_price(stat['attributes']["avg_price"], stat['attributes']['payment_asset']['code']),
        "max_price": format_price(stat['attributes']["max_price"], stat['attributes']['payment_asset']['code']),
        "min_price": format_price(stat['attributes']["min_price"], stat['attributes']['payment_asset']['code']),
        "volume": format_price(stat['attributes']["volume"], stat['attributes']['payment_asset']['code'])
    })
  return {"data":sorted(out, key=lambda x: Decimal(x[param][:-4]), reverse=True)}


def getContract(contract_address:str) -> dict:
  endpoint = f'https://api.rarify.tech/data/contracts/{contract_address}'
  response = requests.get(endpoint, headers=RARIFY_header, params={"include":"metadata"}).json()
  token_meta = response['data']
  dsc = ""
  if "description" in token_meta['attributes']:
    dsc = token_meta['attributes']['description']
  return {
    "address": f"0x{token_meta['attributes']['address']}",
    "name": token_meta['attributes']['name'],
    "tokens": token_meta['attributes']['tokens'],
    "unique_owners": token_meta['attributes']['unique_owners'],
    "description": dsc,
    "id": token_meta['id']
  }


def getPriceHistory(contract_address:str, time_period:str):
  """Gets the price history for the given contract for the specified time period as an array of (x, y) coordinates.

  Parameters
  ----------
  contract_address:str
      The address of the contract as specified by Rarify.

  time_period:str
      The time period desired. Formats accepted are '24h', '7d', '30d', 'all_time'

  Returns:
  An array of (x, y) coordinates with x as datetime and y as the price values (avg, min, max, volume)
  """
  endpoint = f"https://api.rarify.tech/data/contracts/{contract_address}/insights/{time_period}"
  response = requests.get(endpoint, headers=RARIFY_header).json()
  print(response)
  return {"data": response['included'][-1]['attributes']['history']}


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

API_key = os.environ.get('TWITTER_API_KEY')
API_Secret = os.environ.get('TWITTER_API_SECRET')
Bearer_Token = os.environ.get('TWITTER_BEARER_TOKEN')
search_url = "https://api.twitter.com/2/tweets/search/recent"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': '(luna) (lang:en)',
    #'tweet_mode' : 'extended',
    'max_results': '20',
    'tweet.fields': 'created_at,lang'}
# query_params = {'query': '(from:twitterdev -is:retweet) OR #twitterdev','tweet.fields': 'author_id'}

def getSentiment(name):
  """
  Takes in String name of token,
  Returns tuple of sentimentScore(float from 0 to 1), and sentimentRatio(float from 0 to 1) (percentage of positive sentiments)
  """
  API_key = "dSnZQuCPMVQfCXGhhgWJ6qs8s"
  API_Secret = "uwgDp27NZ2sEsHfV7oGY95Dy0di38mhQDs9FjzJSfM6n2ejfSr"
  Bearer_Token = "AAAAAAAAAAAAAAAAAAAAAAgQcgEAAAAAtvIEDNCuREcrZhCu3j9F%2FmhXz00%3DQdawgUlRgpvd2eMyeAug3tPY89yuWvjqVV7NWXlvQX00CJIauI"
  search_url = "https://api.twitter.com/2/tweets/search/recent"

  # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
  # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
  query_params = {'query': (name) + '(lang:en)',
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


  sentimentRatio = 0
  avgScore = 0
  length = len(array)
  for i in range(length):
      sentiment, score = analyse(array[i])
      #if-else needed because to convert score to negative
      if sentiment == 'POSITIVE':
          sentimentRatio += 1
          avgScore += score
      else:
          avgScore -= score
  return avgScore/length, sentimentRatio/length


def getPastSentiment(name, time):
  """
  Input: String : Name of collection, Integer : Time in minutes
  Output: Same as getSentiment(name)
  """
  endpoint = 'https://api.twitter.com/2/tweets/search/recent'
  headers = {'authorization': f'Bearer {Bearer_Token}'}
  params = {
      'query': name + '(lang:en)',
      'max_results': '100',
      'tweet.fields': 'created_at, lang'
  }

  dtformat = '%Y-%m-%dT%H:%M:%SZ'

  def time_travel(now, mins):
      now = datetime.strptime(now, dtformat)
      back_in_time = now - timedelta(minutes=mins)
      return back_in_time.strftime(dtformat)

  now = datetime.now()
  last_week = now - timedelta(days=7)
  now = now.strftime(dtformat)

  pre60 = time_travel(now, time)
  params['start_time'] = pre60
  params['end_time'] = now

  return getSentiment(name)

