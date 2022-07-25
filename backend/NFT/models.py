from ctypes.wintypes import POINT
from decimal import Decimal
from pathlib import WindowsPath

from django.db import models

from .mnemonic_query import contract_details, owners_count_by_contract, tokens_supply_by_contract


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
        return collection

    def __str__(self):
        return f"{self.name} | {self.address}"

    def update(self):
        """Update and create new timeseries records, if needed.
        """
        pass


# wip
class Asset(models.Model):
    ENCODED = "encoded"
    URL = "url"
    Type = (
        (ENCODED, 'Encoded'),
        (URL, 'URL')
    )
    parent_collection = models.OneToOneField(Collection, on_delete=models.CASCADE)
    token_id = models.DecimalField(max_digits=10, decimal_places=0,
                                    default=Decimal('0.00'))
    type = models.CharField(
        max_length=7, choices=Type, default=URL, blank=False)

    data = models.TextField(max_length=100_000)

    @classmethod
    def create(cls, raw_uri):
        asset = cls(data=raw_uri)
        return asset


# wip
class DataPoint(models.Model):
    """Represent the necessary historical points for this collection.
    """
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    trf_values = ["minted", "burned", "totalMinted", "totalBurned"]
    prc_values = ["min", "max", "avg"]
    vol_values = ["count", "volume"]

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['collection', 'timestamp'], name="%(app_label)s_%(class)s_unique")
            ]

    @classmethod
    def create(cls, collection, timestamp):
        """Initialise the fields as given.

        WORK IN PROGRESS
        """
        point = cls(collection=collection, timestamp=timestamp)
        point.save()
        return point



