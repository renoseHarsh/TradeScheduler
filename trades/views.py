import json

import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from .form import ScheduledTradeForm
from .models import ScheduledTrade

BASE_URL = "https://api-fxpractice.oanda.com"


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
            trade.delete()
    return redirect("dashboard:index")


@csrf_exempt
def execute(request):
    data = json.loads(request.body.decode("utf-8"))
    trade_id = data["data"]["trade_id"]
    trade = ScheduledTrade.objects.get(id=trade_id)
    token = trade.user.accesstoken.token
    account_id = trade.user.accesstoken.customer_id
    instrument = trade.pair

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept-Datetime-Format": "RFC3339",
        "Content-Type": "application/json",
    }

    url = BASE_URL + f"/v3/accounts/{account_id}/pricing?instruments={instrument}"
    response = requests.get(url, headers=headers)
    data = response.json()["prices"][0]
    buy_price = float("inf")
    sell_price = float("-inf")

    for bid in data["bids"]:
        sell_price = max(sell_price, float(bid["price"]))
    for ask in data["asks"]:
        buy_price = min(buy_price, float(ask["price"]))

    take_profit = round(buy_price + (float(trade.take_profit) * 0.0001), 5)
    stop_loss = round(buy_price - (float(trade.stop_loss) * 0.0001), 5)

    url = BASE_URL + f"/v3/accounts/{account_id}/orders"
    payload = json.dumps(
        {
            "order": {
                "type": "MARKET",
                "instrument": instrument,
                "units": trade.units,
                "takeProfitOnFill": {
                    "price": f"{take_profit}",
                },
                "stopLossOnFill": {
                    "price": f"{stop_loss}",
                },
            }
        }
    )
    response = requests.post(url, headers=headers, data=payload)

    return JsonResponse({"status": "success"})
