import json
from datetime import timedelta

import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.timezone import now

from trades.models import ScheduledTrade

# Create your views here.


@login_required(login_url="/users/login/")
def index(request):

    cur_time = now()
    future_time = cur_time + timedelta(minutes=1)

    url = "https://api.posthook.io/v1/hooks"
    payload = json.dumps(
        {
            "path": "trades/execute/",
            "postAt": future_time.isoformat(),
            "data": {"trade_id": "OMG NO WAY"},
        }
    )
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": "e01bdf82f59c4ca6b137abe8a39964d3",
    }
    requests.request("POST", url, headers=headers, data=payload)
    trades = ScheduledTrade.objects.filter(user=request.user).order_by("scheduled_time")
    return render(request, "dashboard/index.html", {"data": trades})
