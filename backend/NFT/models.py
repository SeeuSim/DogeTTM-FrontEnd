from urllib.request import urlopen

from django.db import models
from django.utils import timezone

from .mnemonic_query import (contract_details, contract_tokens, format_date,
                             owners_count_by_contract, price_history,
                             sales_volume_by_contract,
                             tokens_supply_by_contract)


# Create your models here.
# wip
class Collection(models.Model):
    name = models.CharField(max_length=512)
    address = models.CharField(max_length=42, unique=True)
    owners = models.BigIntegerField(default=0)
    token_count = models.BigIntegerField(default=0)

    init_state = {
        "1d": '-1',
        "7d": '-1',
        '30d': '-1',
        '365d': '-1'
    }

    avg_price = models.JSONField(default=dict)
    max_price = models.JSONField(default=dict)
    sales_count = models.JSONField(default=dict)
    sales_volume = models.JSONField(default=dict)

    last_updated = models.DateTimeField(default=timezone.now)


    @classmethod
    def create(cls, address_input):
        """Initialise the related models and update those fields.

        1. Retrieve metadata (name, description if possible)
        2. Retrieve asset
        3. Retrieve time series data and initialise records
            3.1. Retrieve Transfers
            3.2. Retrieve Prices
            3.3. Retrieve Volume Points
        """
        collection = cls(address=address_input)
        collection.name = contract_details(address_input)['contract']['name']
        owners = owners_count_by_contract(
            address_input, "DURATION_1_DAY", "GROUP_BY_PERIOD_15_MINUTES")['dataPoints'][-1]['count']
        token_data = tokens_supply_by_contract(
            address_input, "DURATION_1_DAY", "GROUP_BY_PERIOD_15_MINUTES")['dataPoints'][-1]
        minted:int = int(token_data['totalMinted'])
        burned:int = int(token_data['totalBurned'])

        collection.owners = collection.__absolute_bigint(int(owners))
        collection.token_count = collection.__absolute_bigint(minted - burned)

        for item in [collection.avg_price, collection.max_price,
                collection.sales_count, collection.sales_volume]:
            item = collection.init_state
        collection.save()
        Asset.create(collection)
        collection.populate_datapoints()
        return collection


    def __absolute_bigint(self, value):
        if value < 0:
            return max(value, -9223372036854775807)
        else:
            return min(value, 9223372036854775807)


    def refresh_timeseries(self):
        prices = price_history(self.address, "DURATION_7_DAYS", "GROUP_BY_PERIOD_1_DAY")['dataPoints']
        volume = sales_volume_by_contract(self.address, "DURATION_7_DAYS", "GROUP_BY_PERIOD_1_DAY")['dataPoints']
        tokens = tokens_supply_by_contract(self.address, "DURATION_7_DAYS", "GROUP_BY_PERIOD_1_DAY")['dataPoints']
        for index, point in enumerate(prices):
            self.__update_timeseries(point, "price")
            self.__update_timeseries(volume[index], "volume")
            self.__update_timeseries(tokens[index], "tokens")
        self.last_updated = format_date(prices[-1]['timestamp'])


    def populate_datapoints(self):
        address = self.address
        prices = price_history(address, "DURATION_7_DAYS", "GROUP_BY_PERIOD_1_DAY")['dataPoints']
        volume = sales_volume_by_contract(address, "DURATION_7_DAYS", "GROUP_BY_PERIOD_1_DAY")['dataPoints']
        tokens = tokens_supply_by_contract(address, "DURATION_7_DAYS", "GROUP_BY_PERIOD_1_DAY")['dataPoints']
        collection = self

        for index, point in enumerate(prices):
            epoch = format_date(point['timestamp'])
            dP = DataPoint.create(collection=collection, timestamp=epoch)

            vol = volume[index]
            tkns = tokens[index]

            for key in dP.prc_values:
                #set price
                dP.prc[key] = point[key]
            for key in dP.vol_values:
                #set volume
                dP.vol[key] = vol[key]
            for key in dP.tkn_values:
                #set token
                dP.tkn[key] = tkns[key]
            dP.save()


    def update_rank(self, data, field, timeperiod):
        """Update rank records.
        """
        data_map = {
            "avg_price": self.avg_price,
            "max_price": self.max_price,
            "sales_count": self.sales_count,
            "sales_volume": self.sales_volume
        }
        timeperiod_map = {
            "DURATION_1_DAY":"1d",
            "DURATION_7_DAYS":"7d",
            "DURATION_30_DAYS":"30d",
            "DURATION_365_DAYS":"365d"
        }
        data_map[field][timeperiod_map[timeperiod]] = data
        self.save()


    def __update_timeseries(self, data, field):
        """Updates the datapoints for their respective fields.

        Params:
        - data: an array of datapoints returned from the Mnemonic API for the
            respective endpoints: Price History, Token Supply, Sales Volume
        - field: "price", "tokens", "volume"
        """
        for point in data:
            epoch = format_date(point['timestamp'])
            if DataPoint.objects.filter(collection=self,timestamp=epoch).exists():
                dP = DataPoint.objects.filter(collection=self,timestamp=epoch)[0]
            else:
                dP = DataPoint.create(collection=self, timestamp=epoch)
            dP.update(point, field)


    def __str__(self):
        return f"{self.name} | {self.address}"


# wip
class Asset(models.Model):
    ENCODED = "encoded"
    URL = "url"
    Type = (
        (ENCODED, 'Encoded'),
        (URL, 'URL')
    )
    parent_collection:Collection = models.OneToOneField(Collection, on_delete=models.CASCADE)
    token_id = models.BigIntegerField(default=0)
    type = models.CharField(
        max_length=7, choices=Type, default=URL, blank=False)

    data = models.TextField(max_length=100_000, default="")
    mimeType = models.CharField(max_length=50, default="")

    @classmethod
    def create(cls, collection):
        asset = cls(parent_collection=collection)
        address = asset.parent_collection.address
        tokens = contract_tokens(address)['tokens']
        for tkn in tokens:
            if tkn['metadata'] and "image" in tkn['metadata'] \
                    and tkn['metadata']['image'] \
                    and 'uri' in tkn['metadata']['image']:
                __data = tkn['metadata']['image']['uri']
                mime_type = tkn['metadata']['image']['mimeType']

                asset.data = asset.process_data(__data, mime_type)
                asset.mimeType = mime_type
                asset.token_id = min(int(tkn['tokenId']), 9223372036854775807)
                break
        asset.save()
        return asset


    def process_data(self, data:str, mimeType:str) -> str:
        if "ipfs" in data[:10]:
            self.type = self.URL
            self.save()
            return data.replace('ipfs://', "https://ipfs.io/ipfs/")
        elif ";" in mimeType or "," in data[:30]:
            self.type = self.ENCODED
            self.save()
            data = data.split(',')[-1]
            mime = mimeType.split(';')[0]
            return f'data:{mime};base64,{data}'
        else:
            self.type = self.URL
            self.save()
            return data


    def __str__(self) -> str:
        return f"Asset: {self.parent_collection.name}|{self.type}|{self.mimeType}"


#wip
class DataPoint(models.Model):
    """Represent the necessary historical points for this collection.
    TODO: Add Sentiment fields
    """
    tkn_values = ["minted", "burned", "totalMinted", "totalBurned"]
    prc_values = ["min", "max", "avg"]
    vol_values = ["count", "volume"]

    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    tkn = models.JSONField()
    prc = models.JSONField()
    vol = models.JSONField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['collection', 'timestamp'], name="%(app_label)s_%(class)s_unique")
            ]

    @classmethod
    def create(cls, collection, timestamp):
        """Initialise the fields as given.
        """
        point = cls(collection=collection, timestamp=timestamp.replace(tzinfo=timezone.utc))
        point.tkn = {key: "" for key in cls.tkn_values}
        point.prc = {key: "" for key in cls.prc_values}
        point.vol = {key: "" for key in cls.vol_values}
        point.save()
        return point

    def update(self, data, metric):
        metric_mappings = {
            "price": self.prc,
            "tokens": self.tkn,
            "volume": self.vol
        }
        for k in metric_mappings[metric]:
            metric_mappings[metric][k] = data[k]
        self.save()

    def __str__(self):
        return f"DataPoint: {self.collection}|{self.timestamp}"

