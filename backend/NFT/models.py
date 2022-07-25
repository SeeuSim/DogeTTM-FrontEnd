from decimal import Decimal

from django.db import models

from .mnemonic_query import (contract_details, contract_tokens,
                             owners_count_by_contract, price_history,
                             sales_volume_by_contract,
                             tokens_supply_by_contract)


# Create your models here.
# wip
class Collection(models.Model):
    name = models.CharField(max_length=512)
    address = models.CharField(max_length=42, unique=True)
    owners = models.BigIntegerField(default=int("0"))
    token_count = models.BigIntegerField(default=int("0"))

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
        collection.owners = owners_count_by_contract(
            address_input, "DURATION_1_DAY", "GROUP_BY_PERIOD_15_MINUTES")['dataPoints'][-1]['count']
        token_data = tokens_supply_by_contract(
            address_input, "DURATION_1_DAY", "GROUP_BY_PERIOD_15_MINUTES")['dataPoints'][-1]
        minted:int = int(token_data['totalMinted'])
        burned:int = int(token_data['totalBurned'])
        collection.token_count = minted - burned
        collection.save()
        Asset.create(collection)
        populate_datapoints(collection)
        return collection

    def __str__(self):
        return f"{self.name} | {self.address}"

    def update(self):
        """Update and create new timeseries records, if needed.
        """
        pass


def populate_datapoints(collection:Collection):
    address = collection.address
    prices = price_history(address, "DURATION_7_DAYS", "GROUP_BY_PERIOD_1_DAY")['dataPoints']
    volume = sales_volume_by_contract(address, "DURATION_7_DAYS", "GROUP_BY_PERIOD_1_DAY")['dataPoints']
    tokens = tokens_supply_by_contract(address, "DURATION_7_DAYS", "GROUP_BY_PERIOD_1_DAY")['dataPoints']
    collection = Collection.objects.filter(address=address)[0]
    for index, point in enumerate(prices):
        epoch = point['timestamp'].replace('T', ' ').replace('Z', '')
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


# wip
class Asset(models.Model):
    ENCODED = "encoded"
    URL = "url"
    Type = (
        (ENCODED, 'Encoded'),
        (URL, 'URL')
    )
    parent_collection:Collection = models.OneToOneField(Collection, on_delete=models.CASCADE)
    token_id = models.DecimalField(max_digits=10, decimal_places=0,
                                    default=Decimal('0.00'))
    type = models.CharField(
        max_length=7, choices=Type, default=URL, blank=False)

    data = models.TextField(max_length=100_000)
    mimeType = models.CharField(max_length=50, default="")

    @classmethod
    def create(cls, collection):
        asset = cls(parent_collection=collection)
        address = asset.parent_collection.address
        tokens = contract_tokens(address)['tokens']
        for tkn in tokens:
            if "image" in tkn['metadata']:
                asset.data = tkn['metadata']['image']['uri']
                asset.mimeType = tkn['metadata']['image']['mimeType']
                break
        asset.save()
        return asset

    def __str__(self) -> str:
        return f"Asset: {self.parent_collection}|{self.mimeType}"


# wip
class DataPoint(models.Model):
    """Represent the necessary historical points for this collection.
    """
    tkn_values = ["minted", "burned", "totalMinted", "totalBurned"]
    prc_values = ["min", "max", "avg"]
    vol_values = ["count", "volume"]

    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    tkn = models.JSONField(default={})
    prc = models.JSONField(default={})
    vol = models.JSONField(default={})

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['collection', 'timestamp'], name="%(app_label)s_%(class)s_unique")
            ]

    @classmethod
    def create(cls, collection, timestamp):
        """Initialise the fields as given.
        """
        point = cls(collection=collection, timestamp=timestamp)
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

