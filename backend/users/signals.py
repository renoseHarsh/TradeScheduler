from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import AccessToken


@receiver(post_save, sender=User)
def create_access_token(sender, instance, created, **kwargs):
    if created:
        AccessToken.objects.create(user=instance)
