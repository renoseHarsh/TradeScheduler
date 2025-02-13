from django.contrib import admin

from .models import AccessToken, Account

# Register your models here.
admin.site.register(AccessToken)
admin.site.register(Account)
