from django import forms

from .models import ScheduledTrade


class ScheduledTradeForm(forms.ModelForm):
    class Meta:
        model = ScheduledTrade
        fields = "__all__"
        exclude = ["user", "created_at", "updated_at"]
