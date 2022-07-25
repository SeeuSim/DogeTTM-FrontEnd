from django.http import JsonResponse
from django.shortcuts import render
from . import mnemonic_query

# Create your views here.
def tokens_by_contract(request, contract_address:str):
    response = JsonResponse(mnemonic_query.contract_tokens(contract_address))
    return response

def token_metadata(request, contract_address:str, token_id:str):
    return JsonResponse(mnemonic_query.token_metadata(contract_address, token_id))

def collection_price_history(request, contract_address:str, time_period:str, grouping:str):
    return JsonResponse(mnemonic_query.price_history(contract_address, time_period, grouping))

def contract(request, contract_address:str):
    return JsonResponse(mnemonic_query.contract_tokens(contract_address))

def collection_price_history_with_sentiment(request, contract_address:str, time_period:str, grouping:str):
    return JsonResponse(mnemonic_query.price_history_with_sentiment(contract_address, time_period, grouping))
