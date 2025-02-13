from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class AccessToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    paper_token = models.CharField(max_length=255, blank=True, null=True)
    live_token = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Account(models.Model):
    ACCESS_TYPE_CHOICES = (
        ("paper", "Paper"),
        ("live", "Live"),
    )
    access_token = models.ForeignKey(AccessToken, on_delete=models.CASCADE)
    account_id = models.CharField(max_length=255)
    account_type = models.CharField(max_length=255, choices=ACCESS_TYPE_CHOICES)

    def __str__(self):
        return f"{self.account_type} for {self.access_token}"
