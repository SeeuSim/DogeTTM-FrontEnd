import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model


def predict(input):
    #Use relative path for VSCode
    model = load_model('../DogeTest2.h5')
    prediction = model.predict(input)
    return prediction

def getNextDayPriceIncrease(arr):
    nparr = np.array([arr])
    nparr = nparr.reshape(-1,1)
    p = predict(nparr)
    price_incr = p[-1][0] * 100     #last element is predicted next day price, x100 for percentage rise from today
    price_incr = float(("{:.3f}".format(price_incr)))
    return price_incr

def getNextWeekPriceIncrease(arr): #percentage increase for next n days, n being input size of arr
    nparr = np.array([arr])
    nparr = nparr.reshape(-1,1)
    p = predict(nparr)
    output = []
    for x in p:
        price_incr = x[0]*100
        price_incr = float(("{:.3f}".format(price_incr)))
        output.append(price_incr)
    return output

testArr = [0.2,0.7, -0.9, -0.8, 0.5]
#print(getNextDayPriceIncrease(testArr))
print(getNextWeekPriceIncrease(testArr))
