from django.core.management import BaseCommand

from apps.staff.models import Request_price


class Command(BaseCommand):

    def updateRequestStatus(self):
        Request_price.objects.filter(answer=True).update(status=Request_price.Status.ACCEPTED)

    def handle(self, *args, **options):
        self.updateRequestStatus()
