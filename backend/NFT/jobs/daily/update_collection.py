from django_extensions.management.jobs import BaseJob
from django.utils import timezone
from datetime import timedelta
from ... import models
from ....dashboard import mnemonic_query

class Job(BaseJob):
    help = "Refreshes all timeseries and rank data within the database"

    def execute(self):
        current_time = timezone.now()
        for collection in models.Collection.objects.all():
            if current_time - collection.last_updated > timedelta(days=7):
                collection.refresh_timeseries()

        metric_to_query = {
            'avgPrice': "by_avg_price",
            'maxPrice': "by_max_price",
            'salesCount': "by_sales_count",
            'salesVolume': "by_sales_volume"
        }

        metric_headers = ['avgPrice', 'maxPrice', 'salesCount', 'salesVolume']
        for collection in models.Collection.objects.all():
            for i in metric_headers:
                collection.update_rank(float('-int'), metric_to_query[i][3:], "DURATION_7_DAYS")

        for i in metric_headers:
            collections_list = mnemonic_query.get_top_collections(metric_to_query[i], "DURATION_7_DAYS")['collections']
            for collection in collections_list:
                c_address = collection['contractAddress']
                filt = models.Collection.objects.filter(address=c_address)
                if filt.exists():
                    col = filt[0]
                else:
                    col = models.Collection.create(address_input=c_address)
                col.update_rank(collection[i], metric_to_query[i][3:], "DURATION_7_DAYS")



