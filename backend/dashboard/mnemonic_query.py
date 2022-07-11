"""
Hosts all helper functions on NFT data from the Mnemonic API.

Top Collections Ranking:
by_avg_price
by_max_price
by_sales_count
by_sales_volume
"""

import json
import os
from urllib.request import urlopen

import dotenv
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse

dotenv.load_dotenv()
MNEMONIC_KEY = os.getenv('MNEMONIC_KEY')

HEADER = {
    "X-API-Key": MNEMONIC_KEY
}

def get_top_collections(metric:str, time_period:str) -> dict:
    """Gets the top ranked collections from the Mnemonic API, by the following metrics and time periods:

    Ranking:
    - by_avg_price
    - by_max_price
    - by_sales_count
    - by_sales_volume

    Time Period:
    - DURATION_UNSPECIFIED: Unspecified value.
    - DURATION_1_DAY: 1 day.
    - DURATION_7_DAYS: 7 days.
    - DURATION_30_DAYS: 30 days.
    - DURATION_365_DAYS: 365 days.
    """
    mnemonic_endpoint:str = f"https://ethereum.rest.mnemonichq.com/collections/v1beta1/top/{metric}"

    param = {
        "duration": f"{time_period}",
        "limit": "500"
    }
    print('requesting')
    return requests.get(mnemonic_endpoint, headers=HEADER, params=param).json()

def get_top_collections_client(data:JsonResponse, metric:str) -> list:
    """Returns a list of the top tokens in a format for the frontend client.

    With similar parameters to ::get_top_collections, serves the data as a List
    of 10 tokens for the frontend client.
    """

    result_keys = {
        "by_avg_price": 'avgPrice',
        "by_max_price": 'maxPrice',
        "by_sales_count": 'salesCount',
        "by_sales_volume": 'salesVolume'
    }
    key = result_keys[metric]
    client_list = json.loads(data.content.decode())['collections'][:10]

    return list(map(lambda token: [get_contract_art(token['contractAddress']), token['contractName'], token[key]], client_list))

def process(image_uri:str, image_mimeType:str) -> tuple:
    if "ipfs" in image_uri[:10]:
        return (image_uri.replace("ipfs://", "ipfs.io/ipfs/"), "url")
    elif 'base64' in image_mimeType:
        return (urlopen(
            f'data:{image_mimeType}, {image_uri}')
            .read().decode().split(",")[-1], "raw")
    elif 'data' in image_uri[:10]:
        return (urlopen(image_uri).read().decode(), "raw")

    else:
        return (image_uri, "url")


def get_contract_art(contract_address:str) -> tuple:
    mnemonic_endpoint = f"https://ethereum.rest.mnemonichq.com/tokens/v1beta1/by_contract/{contract_address}"
    param = {
        "limit": "10",
        "sortDirection": "SORT_DIRECTION_ASC"
    }
    data = requests.get(mnemonic_endpoint, headers=HEADER, params=param).json()
    image = {
        "uri": "",
        "mimeType": ""
    }
    if "tokens" in data:
        data = data['tokens']
        for token in data:
            if "metadata" in token and "image" in token['metadata'] and token['metadata']['image']:
                image['uri'] = token['metadata']['image']['uri']
                image['mimeType'] = token['metadata']['image']['mimeType']
                break

    if image['uri'] and image['mimeType']:
        return process(image['uri'], image['mimeType'])
    else:
        return ("", "url")



