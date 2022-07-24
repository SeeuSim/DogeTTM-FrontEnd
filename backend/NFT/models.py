from decimal import Decimal
from pathlib import WindowsPath

from django.db import models


# Create your models here.
@wip
class Collection(models.Model):
    name = models.CharField(max_length=512)
    address = models.CharField(max_length=42)
    asset = models.ForeignKey('Asset', on_delete=models.PROTECT)


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
        return collection

    def update(self):
        """Update and create new timeseries records, if needed.
        """
        pass


@wip
class Asset(models.Model):
    ENCODED = "encoded"
    URL = "url"
    Type = (
        (ENCODED, 'Encoded'),
        (URL, 'URL')
    )
    collection = models.OneToOneField('Collection', on_delete=models.CASCADE)
    token_id = models.DecimalField(max_digits=10, decimal_places=0,
                                    default=Decimal('0.00'))
    type = models.CharField(
        max_length=7, choices=Type, default=URL, blank=False)

    data = models.TextField(max_length=100_000)

    @classmethod
    def create(cls, raw_uri):
        asset = cls(data=raw_uri)
        return asset


@wip
class DataPoint(models.Model):
    """Represent the necessary historical points for this collection.
    """
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    trf_values = ["minted", "burned", "totalMinted", "totalBurned"]
    prc_values = ["min", "max", "avg"]
    vol_values = ["count", "volume"]

    @classmethod
    def create(cls, data):
        """Initialise the fields as given.

        WORK IN PROGRESS
        """
        pass


