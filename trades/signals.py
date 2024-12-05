import json
from datetime import timezone

import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from .models import ScheduledTrade


@receiver(post_save, sender=ScheduledTrade)
def send_hook_after_save(sender, instance, created, **kwargs):
    if created:
        url = "https://api.posthook.io/v1/hooks"
        payload = json.dumps(
            {
                "path": "trades/execute/",
                "postAt": instance.scheduled_time.isoformat(),
                "data": {"trade_id": instance.id},
            }
        )
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": "e01bdf82f59c4ca6b137abe8a39964d3",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        data = json.loads(response.text)
        instance.hook_id = data["data"]["id"]
        instance.save()
