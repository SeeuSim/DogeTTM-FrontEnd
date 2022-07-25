import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model

def predict(input):
    #Use relative path for VSCode
    model = load_model('C:/Users/Liu Zixin/Documents/GitHub/DogeTTM-FrontEnd/backend/DogeTest1.h5')
    prediction = model.predict(input)
    return prediction

def getNextDayPriceIncrease(arr):
    nparr = np.array([arr])
    nparr = nparr.reshape(-1,1)
    p = predict(nparr)
    return p[-1][0] * 100     #last element is predicted next day price, *100 for percentage rise from today

def getNextWeekPriceIncrease(arr):
    nparr = np.array([arr])
    nparr = nparr.reshape(-1,1)
    p = predict(nparr)
    output = []
    for x in p:
        output.append(x[0]*100)
    return output

#testArr = [0.3,0.2,-0.8,0.7,0.3]
#print(getNextDayPriceIncrease(testArr))
#print(getNextWeekPriceIncrease(testArr))
