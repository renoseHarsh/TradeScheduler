# from APscheduler.scheduler import get_scheduler
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ScheduledTrade
from .tasks import execute_trade


@receiver(post_save, sender=ScheduledTrade)
def send_hook_after_save(sender, instance, created, **kwargs):
    if created or not instance.task_id:
        task_id = execute_trade.apply_async(
            args=[instance.id], eta=instance.scheduled_time
        )
        instance.task_id = task_id
        instance.save()
