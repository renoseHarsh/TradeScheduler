from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.forms import ValidationError
from django.utils.timezone import now
from users.models import Account


# Create your models here.
class ScheduledTrade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    PAIR_CHOICES = [
        ("EUR_USD", "EURUSD"),
        ("AUD_USD", "AUDUSD"),
        ("USD_JPY", "USDJPY"),
        ("USD_CAD", "USDCAD"),
        ("NZD_USD", "NZDUSD"),
        ("AUD_JPY", "AUDJPY"),
        ("USD_CHF", "USDCHF"),
    ]
    pair = models.CharField(
        max_length=20, choices=PAIR_CHOICES, null=False, blank=False
    )
    units = models.IntegerField(
        validators=[MinValueValidator(1)], null=True, blank=True
    )
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.000000001")),
            MaxValueValidator(Decimal("100")),
        ],
        null=True,
        blank=True,
    )
    take_profit = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.09"))],
    )
    stop_loss = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.09"))],
    )
    scheduled_time = models.DateTimeField(null=False, blank=False)
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    ACTION_CHOICES = [
        ("buy", "buy"),
        ("sell", "sell"),
    ]
    action = models.CharField(
        max_length=4, choices=ACTION_CHOICES, null=False, blank=False
    )
    status = models.CharField(max_length=70, default="scheduled")
    task_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.pair} at {self.scheduled_time}"

    def clean(self, *args, **kwargs):
        super(ScheduledTrade, self).clean(*args, **kwargs)
        if self.units and self.percentage:
            raise ValidationError("You can only set units or percentage, not both")
        if not self.units and not self.percentage:
            raise ValidationError("You must set units or percentage")
        if not self.pk:
            if self.scheduled_time <= now():
                raise ValidationError("Scheduled time must be in the future")
