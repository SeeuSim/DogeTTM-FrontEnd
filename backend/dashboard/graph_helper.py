#Copy pasting over from notebook once I'm done 
import matplotlib.pyplot as plt
import pandas as pd
from . import price_helper 
def graphPastSentiment(name, days):

    #to be stored in .env    
    API_key = "dSnZQuCPMVQfCXGhhgWJ6qs8s"
    API_Secret = "uwgDp27NZ2sEsHfV7oGY95Dy0di38mhQDs9FjzJSfM6n2ejfSr"
    Bearer_Token = "AAAAAAAAAAAAAAAAAAAAAAgQcgEAAAAAtvIEDNCuREcrZhCu3j9F%2FmhXz00%3DQdawgUlRgpvd2eMyeAug3tPY89yuWvjqVV7NWXlvQX00CJIauI"
    search_url = "https://api.twitter.com/2/tweets/search/recent"

    daysArr = []
    priceArr = []
    sentimentArr = []
    for i in range(days):
        daysArr.append(i+1) #X-axis: Days array in a week
        currSentiments = getPastSentiment(name, (7-i+1) * 1440) #With day 7 as current day, start from day 0, 
                                                                #so first day will be (7-1+1) * 1440 minutes in the past
        sentimentArr.append(currSentiments[0])                    #currSentiments return a tuple of (sentimentScore, sentimentRatio), 
                                                                #we want sentimentScore as Y-Axis here
    plt.title('Sentiment of ' + name + ' over ' + str(days) + ' days')
    plt.xlabel('Days')
    plt.ylabel('Sentiment Score')
    plt.plot(daysArr, sentimentArr)

