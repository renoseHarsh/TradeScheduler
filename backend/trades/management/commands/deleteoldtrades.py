from django.core.management import BaseCommand

from ...models import ScheduledTrade


class Command(BaseCommand):
    help = "Deletes all old scheduled trades"

    def handle(self, *args, **options):
        ScheduledTrade.objects.filter(status="scheduled").delete()
