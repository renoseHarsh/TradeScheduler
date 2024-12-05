from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from trades.models import ScheduledTrade

# Create your views here.


@login_required(login_url="/users/login/")
def index(request):
    trades = ScheduledTrade.objects.filter(user=request.user).order_by(
        "-scheduled_time"
    )

    return render(request, "dashboard/index.html", {"data": trades})
