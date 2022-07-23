from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from . import mnemonic_query


@cache_page(60 * 60)
def top_collections(request, metric:str, time_period:str):
    return JsonResponse(mnemonic_query.get_top_collections(metric, time_period))


@cache_page(60 * 60)
def top_collections_client(request, metric:str, time_period:str):
    return JsonResponse(mnemonic_query.get_top_collections_client(
        top_collections(request, metric, time_period), metric), safe=False)

