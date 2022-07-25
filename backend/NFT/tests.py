from django.test import TestCase
from .models import *
from psycopg2.errors import UniqueViolation

# Create your tests here.

class CollectionTest(TestCase):

    def unique_collection_address(self):
        test = Collection.create("test_address")
        try:
            test2 = Collection.create("test_address")
            assert not test2
        except UniqueViolation:
            Collection.objects.filter(address="test_address").delete()
            assert True


"""
class AssetTest(TestCase):
    def unique_asset

class DataPointTest(TestCase):

"""
