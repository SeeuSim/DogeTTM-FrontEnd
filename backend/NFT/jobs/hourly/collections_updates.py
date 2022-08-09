from django_extensions.management.jobs import HourlyJob


class Job(HourlyJob):
    help = "runs updates on the entire database of collections to align with \
        latest ranking"
    def execute(self):
        return super().execute()

