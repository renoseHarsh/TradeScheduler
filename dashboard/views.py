import json

import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from trades.models import ScheduledTrade

# Create your views here.


@login_required(login_url="/users/login/")
def index(request):
    trades = ScheduledTrade.objects.filter(user=request.user).order_by("scheduled_time")
    return render(request, "dashboard/index.html", {"data": trades})
