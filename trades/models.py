from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.forms import ValidationError
from django.utils.timezone import now


# Create your models here.
class ScheduledTrade(models.Model):
    PAIR_CHOICES = [
        ("EUR_USD", "EUR_USD"),
        ("AUD_USD", "AID_USD"),
        ("GBP_USD", "GBP_USD"),
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
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        null=True,
        blank=True,
    )
    take_profit = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
    )
    stop_loss = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
    )
    scheduled_time = models.DateTimeField(null=False, blank=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    hood_id = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.pair} at {self.scheduled_time}"

    def clean(self):
        if self.units and self.percentage:
            raise ValidationError("You can only set units or percentage, not both")
        if not self.units and not self.percentage:
            raise ValidationError("You must set units or percentage")
        if self.scheduled_time <= now():
            raise ValidationError("Scheduled time must be in the future")
