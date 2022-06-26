from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse
import requests;
import price_helper.py

def topSentiments(request, param:str):
    return getSentiment()
    #to-do add address and time as param, but this is good enough for MVP

def singleCollection(request, param:str):
    #to-do function argument
    return viewIndividualNFTData(request)

#def predict(request, param:str):
