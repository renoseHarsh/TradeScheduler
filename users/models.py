from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class AccessToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
