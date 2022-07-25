import os

import dotenv
import requests

dotenv.load_dotenv()
MNEMONIC_KEY = os.getenv('MNEMONIC_KEY')
HEADER = {
        "X-API-Key": MNEMONIC_KEY
    }
BASE_ENDPOINT = "https://ethereum.rest.mnemonichq.com"

def contract_tokens(contract_address:str):
    mnemonic_endpoint = f'https://ethereum.rest.mnemonichq.com/tokens/v1beta1/by_contract/{contract_address}'

    param = {
        "sortDirection": "SORT_DIRECTION_ASC"
    }

    return requests.get(mnemonic_endpoint, headers=HEADER, params=param).json()

def token_metadata(contract_address:str, token_id:str):
    mnemonic_endpoint = f'https://ethereum.rest.mnemonichq.com/tokens/v1beta1/token/{contract_address}/{token_id}/metadata'

    return requests.get(mnemonic_endpoint, headers=HEADER).json()


def price_history(contract_address:str, time_period:str, grouping:str):
    """Gets the price history for the specified contract address.

    Price history for time periods specified as following:
    - DURATION_UNSPECIFIED: Unspecified value.
    - DURATION_1_DAY: 1 day.
    - DURATION_7_DAYS: 7 days.
    - DURATION_30_DAYS: 30 days.
    - DURATION_365_DAYS: 365 days.

    Grouping of datapoints as specified for the following:
    - GROUP_BY_PERIOD_1_HOUR: 1 hour.
    - GROUP_BY_PERIOD_1_DAY: 1 day.
    """
    mnemonic_endpoint = f'https://ethereum.rest.mnemonichq.com/pricing/v1beta1/prices/by_contract/{contract_address}'
    param = {
        'duration': time_period,
        'groupByPeriod': grouping
    }
    return requests.get(mnemonic_endpoint, headers=HEADER, params=param).json()


def sales_volume_by_contract(contract_address:str, time_period:str, grouping:str) -> dict:
    """Gets the price history for the specified contract address.

    Price history for time periods specified as following:
    - DURATION_UNSPECIFIED: Unspecified value.
    - DURATION_1_DAY: 1 day.
    - DURATION_7_DAYS: 7 days.
    - DURATION_30_DAYS: 30 days.
    - DURATION_365_DAYS: 365 days.

    Grouping of datapoints as specified for the following:
    - GROUP_BY_PERIOD_1_HOUR: 1 hour.
    - GROUP_BY_PERIOD_1_DAY: 1 day.
    """
    mnemonic_endpoint = f'{BASE_ENDPOINT}/pricing/v1beta1/volumes/by_contract/{contract_address}'
    param = {
        'duration': time_period,
        'groupByPeriod': grouping
    }
    return requests.get(mnemonic_endpoint, headers=HEADER, params=param).json()


def owners_count_by_contract(contract_address:str, duration:str, grouping:str) -> dict:
    """Retrieve the owner count for the specified collection.

    Durations:
    - DURATION_1_DAY
    - DURATION_7_DAYS
    - DURATION_30_DAYS
    - DURATION_365_DAYS

    Groupings:
    - GROUP_BY_PERIOD_15_MINUTES
    - GROUP_BY_PERIOD_1_HOUR
    - GROUP_BY_PERIOD_1_DAY
    """
    mnemonic_endpoint = f'{BASE_ENDPOINT}/collections/v1beta1/owners_count/{contract_address}'
    param = {
        'duration': duration,
        'groupByPeriod': grouping
    }
    return requests.get(mnemonic_endpoint, headers=HEADER, params=param).json()


def tokens_supply_by_contract(contract_address:str, duration:str, grouping:str) -> dict:
    """Retrieve the token supply for the specified collection.

    Durations:
    - DURATION_1_DAY
    - DURATION_7_DAYS
    - DURATION_30_DAYS
    - DURATION_365_DAYS

    Groupings:
    - GROUP_BY_PERIOD_15_MINUTES
    - GROUP_BY_PERIOD_1_HOUR
    - GROUP_BY_PERIOD_1_DAY
    """
    mnemonic_endpoint = f'{BASE_ENDPOINT}/collections/v1beta1/supply/{contract_address}'
    param = {
        'duration': duration,
        'groupByPeriod': grouping
    }
    return requests.get(mnemonic_endpoint, headers=HEADER, params=param).json()


def contract_details(contract_address:str) -> dict:
    mnemonic_endpoint = f'{BASE_ENDPOINT}/contracts/v1beta1/by_address/{contract_address}'
    return requests.get(mnemonic_endpoint, headers=HEADER).json()
