from django_extensions.management.jobs import BaseJob


class Job(BaseJob):
    help = "runs updates on the entire database of collections to align with \
        latest ranking"
    def execute(self):
        return super().execute()

