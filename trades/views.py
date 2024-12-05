from datetime import timedelta

import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt

from .form import ScheduledTradeForm
from .models import ScheduledTrade

url = "https://api.posthook.io/v1/hooks"


# Create your views here.
@login_required(login_url="users:login")
def schedule(request):
    if request.method == "POST":
        form = ScheduledTradeForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
    return redirect("dashboard:index")


@login_required(login_url="users:login")
def delete(request):
    if request.method == "POST":
        trade = ScheduledTrade.objects.get(id=request.POST.get("trade_id"))
        if trade.user == request.user:
            print(trade)
            trade.delete()
    return redirect("dashboard:index")


@csrf_exempt
def recieve_hook(request):
    current_time = now()
    modified_time = current_time + timedelta(hours=5, minutes=30)
    return JsonResponse({"status": modified_time}, status=200)


def schedule_hook(request):
    idk = requests.post(
        "https://httpbin.org/post", data={"key": "reallllldaaaa"}
    ).json()
    print(idk)
    if request.method == "POST":
        relative_url = reverse("trades:recieve_hook")
        full_url = request.build_absolute_uri(relative_url)
        print(full_url)
    return render(request, "trades/index.html")
