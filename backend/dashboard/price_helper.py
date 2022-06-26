#Retrieve all tokens in a collection
import os
import random
from decimal import Decimal
from operator import itemgetter

# from datetime import datetime, timedelta
# import json
# import flair
# import collections

import dotenv
import matplotlib.pyplot as plt
from numpy import add
import pandas as pd
import requests

dotenv.load_dotenv("../frontend/.env")
RARIFY_API_KEY:str = os.environ.get('RARIFY_API_KEY')


def format_price(price:str, currency:str):
  """Prices are in format of 18 decimals"""
  # Returns the price in a readable format, given the 18 decimal raw price

  return f"{(Decimal(price).normalize() * (Decimal('10')**Decimal('-18'))).__str__()} {currency}"


def format_id(tokenID:int) -> str:
  hexID = hex(tokenID)
  if len(hexID) % 2 == 0:
    return hexID[2:]
  return hexID.replace('x', '')

def getart(address:str, tokens:int) -> str:
  tokenid = random.randint(0, tokens)
  hashed_id = format_id(tokenid)
  endpoint = f"https://api.rarify.tech/data/tokens/{address}:{hashed_id}"

  headers = {
      "Authorization": f'Bearer {RARIFY_API_KEY}'
  }
  response = requests.get(endpoint, headers=headers).json()
  if 'image_url' in response['data']['attributes']:
    return response['data']['attributes']['image_url']
  return ""


def get_price_history(address, coin, time_period):
  """Retrieves the price history for a collection in 24h, 7d, 30d, all_time"""
  # 24h: 24 entries 1h apart
  # 7d: 7 entries 1d apart
  # 30d: 30 entries 1d apart
  endpoint = f"https://api.rarify.tech/data/contracts/{coin}:{address[2:]}/insights/{time_period}"
  headers = {
      "Authorization": f'Bearer {RARIFY_API_KEY}'
  }
  response = requests.get(endpoint, headers=headers).json()
  if 'errors' in response:
    return response
  return response['included'][-1]['attributes']['history']


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
      'include': 'insights_trends',
      'sort': '-insights_trends.volume_change_percent',
      'page[limit]': limit
  }
  response = requests.get(endpoint, headers=headers, params=params).json()
  #return response;
  #return [x for x in zip(response['data'], response['included'])]

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
        "imgurl": getart(id, tokens),
        "address": f"0x{token['attributes']['address']}",
        "name": nm,
        "tokens": tokens,
        "unique_owners": token['attributes']['unique_owners'],
        "volume_change": format_price(stat['attributes']['volume_change'],stat['attributes']['payment_asset']['code']),
        "percent_change": stat['attributes']['volume_change_percent']
    })

  return {'data':out}

def get_top(param:str, limit:int) -> dict or list:
  if param not in {"min_price", 'max_price', 'volume'}:
    raise ValueError("wrong param. Choose from 'min_price', 'max_price', or 'volume'")
  if limit < 5:
    limit = 5
  endpoint = 'https://api.rarify.tech/data/contracts'
  headers = {
      "Authorization": f'Bearer {RARIFY_API_KEY}'
  }
  print(RARIFY_API_KEY)

  params = {
      'include': 'insights',
      'sort': f'-insights.{param}',
      'page[limit]': limit
  }

  response = requests.get(endpoint, headers=headers, params=params).json()
  # return response
  return {"data":[x for x in zip(response['data'], response['included'])]}

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

#Takes in String name of token, 
#Returns tuple of sentimentScore(float from 0 to 1), and sentimentRatio(float from 0 to 1) (percentage of positive sentiments)
def getSentiment(name):
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

#print(getSentiment('luna'))

#Input: String : Name of collection, Integer : Time in minutes
#Output: Same as getSentiment(name)
#Input: String : Name of collection, Integer : Time in minutes
#Output: Same as getSentiment(name)
def getPastSentiment(name, time):
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

#print(getPastSentiment('luna', 60))


'''
[{"imgurl": "https://daiakrtkievq7ofrm5xaoecjyjfmsybdd2nxxdm5ey74a4ku6ama.arweave.net/GBAFRmpBKw-4sWduBxBJwkrJYCMem3uNnSY_wHFU8Bg", "address": "0xd1d411d2da363144248b98adab453aa3b19ccf04", "name": "Rug Radio Membership Pass", "tokens": 20000, "unique_owners": 13689, "volume_change": "0.65451 ETH", "percent_change": 333933.7},
{"imgurl": "http://ipfs-proxy.prod.svc.cluster.local/ipfs/QmcaVaNtWDLbsz9EMcb1pLshuzzdUbt9ehWzYq1BP9cPXP/3852.png", "address": "0xc70c411cfdbe542e8208af52092ca4f56b633977", "name": "devilvalley", "tokens": 6665, "unique_owners": 2185, "volume_change": "28.325592 ETH", "percent_change": 212654.6},
{"imgurl": "http://ipfs-proxy.prod.svc.cluster.local/ipfs/QmbS7BhsiNMo3BCyw1LKKo7SgJidvU7ctj2VqDjhTbCJjb/blindbox.png", "address": "0x12073c130ee0612219a0b54e56582ce24155dfa8", "name": "HanfuNFT", "tokens": 5200, "unique_owners": 1424, "volume_change": "5.1386 ETH", "percent_change": 19763.846},
{"imgurl": "https://howlerz.mypinata.cloud/ipfs/QmQMzLa4g5BG6kCjpGPUj3CAHVrSe3EG5SyceD6rwnzryE/3293.png", "address": "0x40cf6a63c35b6886421988871f6b74cc86309940", "name": "HOWLERZ", "tokens": 5000, "unique_owners": 2318, "volume_change": "14.565 ETH", "percent_change": 18206.25},
{"imgurl": "https://kongz.herokuapp.com/static/erc1155/weapons/400x400/cactus_on_a_stick.png", "address": "0x0e28a33728b61a8abe11ac9adc0af17c0d3d7603", "name": "", "tokens": 28, "unique_owners": 364, "volume_change": "909.469241 ETH", "percent_change": 14588.914},
{"imgurl": "http://ipfs-proxy.prod.svc.cluster.local/ipfs/QmTrQGwSNjKx7K8HLp6XFcSYyJJB392rrrECCo4bLADuMS", "address": "0x33857ad1031122a00a68e6bf9ac4475ba6c6f8be", "name": "CandyRobbers", "tokens": 5000, "unique_owners": 2484, "volume_change": "4.0936 ETH", "percent_change": 13645.333},
{"imgurl": "http://ipfs-proxy.prod.svc.cluster.local/ipfs/QmNaKCPFi7KzHiLQ4nU9K8gEZ6gvGLng1jxKMd2GPQ7tuc/6033.png", "address": "0x136b586632497c655c258ee7602c8c6789672319", "name": "Emoji Smile Plz", "tokens": 7777, "unique_owners": 114, "volume_change": "31.88989 ETH", "percent_change": 12755.956},
{"imgurl": "http://ipfs-proxy.prod.svc.cluster.local/ipfs/QmaTmANmWSnLBt3qF1ggtTvsC6J7SsCeYUCsT2fmvzYW9W", "address": "0x2ee6af0dff3a1ce3f7e3414c52c48fd50d73691e", "name": "Bored Ape Yacht Club", "tokens": 9546, "unique_owners": 3792, "volume_change": "59.612977 ETH", "percent_change": 53416.645},
{"imgurl": "http://ipfs-proxy.prod.svc.cluster.local/ipfs/QmQ239zUwimRZjHukrUuTdAjTFCzdcTaQ2ThLD2U8EVGVG", "address": "0x88091012eedf8dba59d08e27ed7b22008f5d6fe5", "name": "Secret Society of Whales", "tokens": 10000, "unique_owners": 3920, "volume_change": "28.827459 ETH", "percent_change": 28827.459},
{"imgurl": "http://ipfs-proxy.prod.svc.cluster.local/ipfs/QmdwxmL59sj5X8bGa2vMeb3rrQTfNM1hnyYsTUdAq61w55/0xcube.gif", "address": "0x5f7b42e237600530e8d286f9c4ef48f5ea5ef518", "name": "0xCubes", "tokens": 1428, "unique_owners": 624, "volume_change": "29.300758 ETH", "percent_change": 18312.975}]
