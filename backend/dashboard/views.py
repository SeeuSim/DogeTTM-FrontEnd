from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse
import requests
from . import price_helper
from . import graph_helper

# def topSentiments(request, param:str):
#     return getSentiment()
#     #to-do add address and time as param, but this is good enough for MVP

#def singleCollection(request, param:str):
#     return viewIndividualNFTData(request)

#def predict(request, param:str):

def plotPastSentiments(request, name:str, days:int):
    return JsonResponse(graph_helper.graphPastSentiment(name, days))

def topRank(request, param:str):
  return JsonResponse(price_helper.get_top(param, 10))

def topTrending(request, period:str):
  return JsonResponse(price_helper.get_trending(10, period))

def getContract(request, contract_id:str):
  return JsonResponse(price_helper.getContract(contract_id))

def getPriceHistory(request, contract_address:str, time_period:str):
  return JsonResponse(price_helper.getPriceHistory(contract_address, time_period))
