from django.http import JsonResponse
from . import models
from . import mnemonic_query


# Create your views here.
def tokens_by_contract(request, contract_address:str):
    response = JsonResponse(mnemonic_query.contract_tokens(contract_address))
    return response


def token_metadata(request, contract_address:str, token_id:str):
    return JsonResponse(mnemonic_query.token_metadata(contract_address,
                                                    token_id))


def collection_price_history(request, contract_address:str, time_period:str,
                            grouping:str):
    return JsonResponse(mnemonic_query.price_history(contract_address,
                                                    time_period,
                                                    grouping))


def contract(request, contract_address:str):
    return JsonResponse(mnemonic_query.contract_tokens(contract_address))


def collection_price_history_with_sentiment(request, contract_address:str,
                                            time_period:str, grouping:str):
    return JsonResponse(mnemonic_query
        .price_history_with_sentiment(contract_address,
                                    time_period,
                                    grouping))


def dashboard_ranking(request, metric:str, time_period:str):
    """Returns the ranking dashboard data for the given metric and time period

    Params:
    - metric: Choose from:
        - avg_price
        - max_price
        - sales_count
        - sales_volume
    - time_period: Choose from:
        - 1d (WIP, will populate server when deployed)
        - 7d
    """
    collection_lib = models.Collection.objects

    order_mappings = {
        "avg_price": {
            "1d": "-avg_price__1d",
            "7d": "-avg_price__7d"
        },
        "max_price": {
            "1d": "-max_price__1d",
            "7d": "-max_price__7d"
        },
        "sales_count": {
            "1d": "-sales_count__1d",
            "7d": "-sales_count__7d"
        },
        "sales_volume": {
            "1d": "-sales_volume__1d",
            "7d": "-sales_volume__7d"
        }
    }

    filter_mappings = {
        "avg_price": {
            "1d": collection_lib.exclude(avg_price__1d=''),
            "7d": collection_lib.exclude(avg_price__7d='')
        },
        "max_price": {
            "1d": collection_lib.exclude(max_price__1d=''),
            "7d": collection_lib.exclude(max_price__7d='')
        },
        "sales_count": {
            "1d": collection_lib.exclude(sales_count__1d=''),
            "7d": collection_lib.exclude(sales_count__7d='')
        },
        "sales_volume": {
            "1d": collection_lib.exclude(sales_volume__1d=''),
            "7d": collection_lib.exclude(sales_volume__7d='')
        }
    }

    data_mappings = {
        "avg_price": lambda collection: collection.avg_price[time_period],
        "max_price": lambda collection: collection.max_price[time_period],
        "sales_count": lambda collection: collection.sales_count[time_period],
        "sales_volume": lambda collection: collection.sales_volume[time_period]
    }

    collections = filter_mappings[metric][time_period].order_by(
        order_mappings[metric][time_period])

    asset_list = {collection.address: models.Asset.objects.get(
        parent_collection=models.Collection.objects.get(
            address=collection.address)) for collection in collections}

    out_list = list(map(
        lambda collection: {
            "artwork": asset_list[collection.address].data,
            "artwork_type": asset_list[collection.address].type,
            "collection_name": collection.name,
            "data": data_mappings[metric](collection),
            "address": collection.address
        }, collections
    ))

    return JsonResponse({"data": out_list})


def search_collections(request, search_field:str, param:str):
    collection_lib = models.Collection.objects
    search_cat_map = {
        "name": collection_lib.filter(name__istartswith=param),
        "address": collection_lib.filter(address__startswith=param)
    }
    return JsonResponse({
        "data": list(map(lambda collection: {
            "name": collection.name,
            "address": collection.address,
            "artwork": models.Asset.objects.get(parent_collection=collection).data
        }, search_cat_map[search_field]))
        })


def searchbar(request):
    return JsonResponse({"data": list(map(lambda collection: \
        {"address": collection.address, "name": collection.name}, 
        models.Collection.objects.all()))})


class CollectionView:
    @staticmethod
    def collection_page(request, contract_address:str):
        return JsonResponse(CollectionView.or_else_create(contract_address))

    @staticmethod
    def collection_as_dict(collection:models.Collection):
        return {
            "name": collection.name,
            "address": collection.address,
            "owners": collection.owners,
            "total_minted": collection.total_minted,
            "total_burned": collection.total_burned,
            "artwork": models.Asset.objects.get(parent_collection=collection).data
        }

    @staticmethod
    def collection_fromdb(contract_address:str):
        collection = models.Collection.objects.get(address=contract_address)
        out = CollectionView.collection_as_dict(collection)
        points = models.DataPoint.objects.filter(collection=collection).order_by('timestamp')
        out['dataPoints'] = list(map(lambda dP: DataPointView.datapoint_as_dict(dP), points))
        return out

    @staticmethod
    def or_else_create(contract_address:str):
        if models.Collection.objects.filter(address=contract_address).exists():
            return CollectionView.collection_fromdb(contract_address)

        try:
            collection = models.Collection.create(contract_address)
        except KeyError:
            assert collection, f'Address `{contract_address}` is invalid. \
                Please provide a valid address.'
        return CollectionView.collection_fromdb(collection.address)


class DataPointView:
    @staticmethod
    def datapoint_as_dict(datapoint:models.DataPoint):
        return {
            "timestamp": datapoint.timestamp,
            "prc": datapoint.prc,
            "tkn": datapoint.tkn,
            "vol": datapoint.vol
        }

