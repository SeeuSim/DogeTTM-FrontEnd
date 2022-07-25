import os
import datetime
import timedelta
import requests
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import sentiment as stm
import tensorflow as tf
import json
import collections
import numpy as np
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from keras.models import load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

"""
Step 1 -> Define get_NFT_name(str contract address) function that gets NFT name based on contract
Step 2 -> Read input and write data of top 500 NFTs, 7 days, 1hr intervals to database (168 * 500 lines + 500 contract addresses = 84.5k lines)
Step 3 -> Iterate through the file and
            1. use get_NFT_name function to replace contract addresses with name strings
            2. call getPastSentiment() from sentiment.py and attach it to corresponding timestamp line (take note of times with 0 price datas)
Step 4 -> Train prediction model using LSTM, with variable X being sentiment 1hr ago, and variable Y being avg price now
Step 5 -> Create 2 prediction models:
            1. Given single point sentiment (past hour), output next hour price
            2. Given multi point sentiment (last 24 hrs), output multi hour price (next 24 hrs)
Step 6 -> Store the output predicted price data into an array, and output as JSON file
"""

API_key = os.environ.get('TWITTER_API_KEY')
API_Secret = os.environ.get('TWITTER_API_SECRET')
Bearer_Token = os.environ.get('TWITTER_BEARER_TOKEN')
RARIFY_API_KEY = os.environ.get('RARIFY_API_KEY')
TWITTER_API_KEY="dSnZQuCPMVQfCXGhhgWJ6qs8s"
TWITTER_API_SECRET="AAAAAAAAAAAAAAAAAAAAAAgQcgEAAAAAtvIEDNCuREcrZhCu3j9F%2FmhXz00%3DQdawgUlRgpvd2eMyeAug3tPY89yuWvjqVV7NWXlvQX00CJIauI"
TWITTER_BEARER_TOKEN="AAAAAAAAAAAAAAAAAAAAAAgQcgEAAAAAtvIEDNCuREcrZhCu3j9F"

search_url = "https://api.twitter.com/2/tweets/search/recent"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': '(name) (lang:en)',
    #'tweet_mode' : 'extended',
    'max_results': '30',
    'tweet.fields': 'created_at,lang'}
    #query_params = {'query': '(from:twitterdev -is:retweet) OR #twitterdev','tweet.fields': 'author_id'}

#Step 1: Define function that converts address into name
def get_NFT_name(address:str):
    RARIFY_API_KEY="1959b00b-435b-4c27-a1b7-66168414d0dc"
    address = "ethereum:" + address
    endpoint = f'https://api.rarify.tech/data/contracts/{address}'
    headers = {
        "Authorization": f'Bearer {RARIFY_API_KEY}'
    }
    params = {
        'include': "metadata"
    }
    response = requests.get(endpoint, headers=headers, params=params)
    return response.json()['data']['attributes']['name']


#Step 2&3: Load dataset and return sentimentArr and priceArr
def loadData(file):
    tf.random.set_seed(7)
    #Get dogeTTM csv file here
    df = pd.read_json(file)
    df = df["data"]
    d1 = datetime.datetime.now()
    nowtime = d1 - datetime.timedelta(days=2.5)
    dtformat = '%Y-%m-%dT%H:%M:%SZ'
    nowt = datetime.datetime.strftime(nowtime, dtformat)
    sentimentArr = []
    priceArr = []
    for i in range(20):    #per token
        address = df[i]['contractAddress']
        try:
            name = get_NFT_name(address)
        except KeyError:
            print("Name not found for " + address)
    data = df[i]['dataPoints']
    tempSentimentArr = []
    tempPriceArr = []
    for j in range(len(data)):     #token data per hour
        try:
            past = data[j]['timestamp']
            if (data[j]['avg'] != "" and past < nowt):    #has price data for that hour
                sentiment = stm.getPastSentimentExact(name, past)
                price = float(data[j]['avg'])
                price = float(("{:.4f}".format(price)))
                print(price)
                print(sentiment[0])
                tempSentimentArr.append(sentiment[0])
                tempPriceArr.append(price)
        except:
            continue

    tempSentimentArr = tempSentimentArr[:-1]  #Make sentiment one step behind price
    tempPriceArr = tempPriceArr[1:]
    sentimentArr.append(tempSentimentArr)
    priceArr.append(tempPriceArr)
    return sentimentArr, priceArr

#Throwing away rows with insufficient data input
def clean(data):
    count = 0
    for x in data:
        if len(x) != len(data[0]):
            print("popping" + str(x))
            X = np.delete(data, count, axis=0)
        count += 1
    return data

def train(input):
    model = Sequential()
    model.add(LSTM(3, input_shape=(5,1)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    sentimentArr, priceArr = loadData(input)
    sentimentArr = clean(sentimentArr)
    priceArr = clean(priceArr)
    print("sentiment arr")
    print(sentimentArr)
    print("price arr")
    print(priceArr)
    for i in range(len(sentimentArr)):
        try:
            X = np.array(sentimentArr[i])
            Y = np.array(priceArr[i])
            X = X.reshape(-1,1)
            Y = Y.reshape(0,1)
            #Normalising price data to -1,1 (in terms of percentage)
            scaler = MinMaxScaler(feature_range=(-1, 1))
            Y = scaler.fit_transform(Y)
            print(X)
            print(Y)
            #Train data
            model.fit(X, Y, epochs=10, batch_size=1, verbose=2)
        except:
            print("Line skipped due to insufficient data")
            continue
    return model

#LOad the 24/07 500tokens 7d file here
model = train("C:/Users/Liu Zixin/Documents/GitHub/DogeTTM-FrontEnd/backend/NFT/test.json")
#testInput = np.array([0,5,0.2,-0.9,0.7,0])
#print(model.predict(testInput))

model.save("DogeTest1.h5")
