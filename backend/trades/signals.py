# from APscheduler.scheduler import get_scheduler
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ScheduledTrade
from .utils import create_hook, execute_trade

# scheduler = get_scheduler()


@receiver(post_save, sender=ScheduledTrade)
def send_hook_after_save(sender, instance, created, **kwargs):
    if created:
        posthook_id = create_hook(instance.id, instance.scheduled_time)
        instance.posthook_id = posthook_id
        instance.save()
