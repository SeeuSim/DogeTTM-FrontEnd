import os
import datetime, timedelta
import requests
import IPython
import IPython.display
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
import sentiment as stm
"""
Step 1 -> Define get_NFT_name(str contract address) function that gets NFT name based on contract
Step 2 -> Read input and write data of top 500 NFTs, 7 days, 1hr intervals to database (168 * 500 lines + 500 contract addresses = 84.5k lines)
Step 3 -> Iterate through the file and
            1. use get_NFT_name function to replace contract addresses with name strings
            2. call getPastSentiment() from sentiment.py and attach it to corresponding timestamp line (take note of times with 0 price datas)
Step 4 -> Train prediction model using RNN, with variableA being sentiment 1hr ago, and variableB being avg price now
Step 5 -> Create 2 prediction models:
            1. Given single point sentiment (past hour), output next hour price
            2. Given multi point sentiment (last 24 hrs), output multi hour price (next 24 hrs)
Step 6 -> Store the output predicted price data into an array, and output as JSON file
"""

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
    #query_params = {'query': '(from:twitterdev -is:retweet) OR #twitterdev','tweet.fields': 'author_id'}

#Step 1: Define function that converts address into name
def get_NFT_name(address:str):
    RARIFY_API_KEY = os.environ.get("RARIFY_API_KEY")
    endpoint = f'https://api.rarify.tech/data/contracts/{address}'
    headers = {
        "Authorization": f'Bearer {RARIFY_API_KEY}'
    }
    params = {
        'include': "metadata"
    }
    response = requests.get(endpoint, headers=headers, params=params)
    return response.json()['data']['attributes']['name']


#Step 2&3: Load dataset and append sentiment
def loadData(file):
    tf.random.set_seed(7)
    #Get dogeTTM csv file here
    df = pd.read_json(file)
    df = df["data"]

    #print(df[0]['contractAddress'])
    now = datetime.now() - timedelta(days=2)
    dtformat = '%Y-%m-%dT%H:%M:%SZ'
    nowt = datetime.strftime(now, dtformat)
    sentimentArr = []
    priceArr = []
    for i in range(10):    #per token
        address = df[i]['contractAddress']
        try:
            name = get_NFT_name(address)
        except KeyError:
            print("Name not found for " + address)
            pass
        data = df[i]['dataPoints']
        tempSentimentArr = []
        tempPriceArr = []
        for j in range(len(data)):     #token data per hour
            past = data[j]['timestamp']
            if (data[j]['avg'] != "" and past < nowt):    #has price data for that hour
                sentiment = stm.getPastSentimentExact(name, past)
                price = float(data[j]['avg'])
                price = float(("{:.4f}".format(price)))
                tempSentimentArr.append(sentiment[0])
                tempPriceArr.append(price)
                print("Time is " + past)
                print("Sentiment is " + str(sentiment[0]))
                print("Price is " + str(price))
        tempSentimentArr = tempSentimentArr[:-1]  #Make sentiment one step behind price
        tempPriceArr = tempPriceArr[1:]
        sentimentArr.append(tempSentimentArr)
        priceArr.append(tempPriceArr)
    return sentimentArr, priceArr

@WIP
def train(xArr, yArr):
    #Partition and normalise Datasets
    sentimentArr = np.array(sentimentArr, dtype = object)
    priceArr = np.array(sentimentArr, dtype = object)

    totalLen = len(sentimentArr)
    trainSize = int(totalLen * 0.7)
    testSize = totalLen - trainSize
    trainS, trainP = sentimentArr[:trainSize], priceArr[:trainSize]
    testS, testP = sentimentArr[trainSize:], priceArr[trainSize:]
    scaler = MinMaxScaler(feature_range=(0, 1))
    #for x in trainP:
    #    trainP = scaler.fit_transform(trainP)

    # create and fit the LSTM network
    from sklearn.linear_model import LinearRegression

    model = Sequential()
    model.add(LSTM(3, input_shape=(5,3)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    for i in range(len(trainS)):
        model.fit(trainS[i], trainP[i], epochs=100, batch_size=1, verbose=2)
    prediction = model.predict(testS)


    #Compromise if LSTM doesn't work
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import PolynomialFeatures
    trainP = np.array(trainP).reshape((-1, 1))
    x_ = PolynomialFeatures(degree=2, include_bias=False).fit_transform(trainP)
    model = LinearRegression().fit(trainS, x_)
