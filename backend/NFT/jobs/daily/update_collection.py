from django_extensions.management.jobs import DailyJob
from django.utils import timezone
from datetime import timedelta

from ... import models, mnemonic_query


class Job(DailyJob):
    help = "Refreshes all timeseries and rank data within the database"

    def execute(self):
        # update timeseries
        threshold_time = timezone.now() - timedelta(days=7)
        for collection in models.Collection.objects.filter(last_updated__lte=threshold_time):
            collection.refresh_timeseries()

        metric_to_query = {
            'avgPrice': "by_avg_price",
            'maxPrice': "by_max_price",
            'salesCount': "by_sales_count",
            'salesVolume': "by_sales_volume"
        }

        metric_headers = ['avgPrice', 'maxPrice', 'salesCount', 'salesVolume']

        # Clear ranking data
        for collection in models.Collection.objects.all():
            for i in metric_headers:
                collection.update_rank('', metric_to_query[i][3:], "DURATION_7_DAYS")

        # Update ranking data
        for i in metric_headers:
            print(i, "\n--------")
            collections_list = mnemonic_query.get_top_collections(metric_to_query[i], "DURATION_7_DAYS")['collections']
            for index, collection in enumerate(collections_list):
                print(index+1, collection['contractName'])
                c_address = collection['contractAddress']
                filt = models.Collection.objects.filter(address=c_address)
                if filt.exists():
                    col = filt[0]
                else:
                    col = models.Collection.create(address_input=c_address)
                col.update_rank(float(collection[i]), metric_to_query[i][3:], "DURATION_7_DAYS")


