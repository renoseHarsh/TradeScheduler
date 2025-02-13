from rest_framework import serializers

from .models import ScheduledTrade


class ScheduledTradeSerializer(serializers.ModelSerializer):
    account_id = serializers.CharField(source="account.account_id", read_only=True)
    account_type = serializers.CharField(source="account.account_type", read_only=True)
    scheduled_time = serializers.DateTimeField(format="%Y-%m-%dT%I:%M %p")

    class Meta:
        model = ScheduledTrade
        exclude = ["account", "user"]


class ScheduleTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledTrade
        fields = [
            "pair",
            "units",
            "percentage",
            "take_profit",
            "stop_loss",
            "scheduled_time",
            "action"
        ]
