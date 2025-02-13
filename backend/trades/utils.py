import hashlib
import hmac
import json
import os
from decimal import ROUND_HALF_UP, Decimal

import requests

from .models import ScheduledTrade

from dotenv import load_dotenv


load_dotenv()

PAPER_URL = "https://api-fxpractice.oanda.com"
LIVE_URL = "https://api-fxtrade.oanda.com"
signature_key = "acd7fe2f12084771b7f3e0e822f57ce2"
POSTHOOK_URL = "https://api.posthook.io/v1"
POSTHOOK_API_KEY = "fBVfOSYAKYcdpPPoDlLz03lL3X3t4jxAiUa4xCmMs-EROW8V9-SqV879eVbH23okx2eys8OoxAHGJxN-E5igJg=="

usd_relation = {
    "EUR": "EUR_USD",
    "AUD": "AUD_USD",
    "JPY": "USD_JPY",
    "CAD": "USD_CAD",
    "NZD": "NZD_USD",
    "CHF": "USD_CHF",
    "ZAR": "USD_ZAR",
}


def get_instrument_price(instrument, account_id, headers, account_type):
    url = f"{PAPER_URL if account_type == 'paper' else LIVE_URL}/v3/accounts/{account_id}/pricing?instruments={instrument}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return -1, -1
    data = response.json()["prices"][0]
    buy_price = float("inf")
    sell_price = float("-inf")
    for bid in data["bids"]:
        sell_price = max(sell_price, float(bid["price"]))
    for ask in data["asks"]:
        buy_price = min(buy_price, float(ask["price"]))

    return Decimal(sell_price), Decimal(buy_price)


def send_request(
    instrument, units, account_id, headers, account_type, take_profit, stop_loss
):
    url = f"{PAPER_URL if account_type == 'paper' else LIVE_URL}/v3/accounts/{account_id}/orders"
    payload = json.dumps(
        {
            "order": {
                "type": "MARKET",
                "instrument": instrument,
                "units": units,
                "takeProfitOnFill": {
                    "distance": str(
                        take_profit.quantize(
                            Decimal("0.01" if "JPY" in instrument else "0.0001"),
                            rounding=ROUND_HALF_UP,
                        )
                    ),
                },
                "stopLossOnFill": {
                    "distance": str(
                        stop_loss.quantize(
                            Decimal("0.01" if "JPY" in instrument else "0.0001"),
                            rounding=ROUND_HALF_UP,
                        )
                    ),
                },
            }
        }
    )
    return requests.post(url, headers=headers, data=payload)


def get_balance(account_id, headers, account_type):
    url = (
        f"{PAPER_URL if account_type == 'paper' else LIVE_URL}/v3/accounts/{account_id}"
    )
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        -1
    return Decimal(response.json()["account"]["balance"])


def get_middle_price(pair, account_id, headers, account_type):
    sell, buy = get_instrument_price(pair, account_id, headers, account_type)
    if sell == -1:
        return -1
    return Decimal((sell + buy) / 2)


def send_percentage_request(trade, account_type, account_id, headers):
    sell_price, buy_price = get_instrument_price(
        trade.pair, account_id, headers, account_type
    )
    if sell_price == -1:
        return -1
    action = 1 if trade.action == "buy" else -1
    pipconv = Decimal(0.0001 if "JPY" not in trade.pair else 0.01)
    balance = get_balance(account_id, headers, account_type)
    if balance == -1:
        return -1
    use = balance * (trade.percentage / 100)
    price = Decimal(buy_price if action == 1 else sell_price)
    take_profit = trade.take_profit * pipconv
    stop_loss = trade.stop_loss * pipconv
    if "USD" in trade.pair:
        if "USD" == trade.pair[:3]:
            units = round(use * action)
        else:
            units = round(use / price) * action
        response = send_request(
            trade.pair, units, account_id, headers, account_type, take_profit, stop_loss
        )
        return response
    else:
        usd_pair = usd_relation[trade.pair[:3]]
        midle_price = get_middle_price(usd_pair, account_id, headers, account_type)
        if midle_price == -1:
            return -1
        if "USD" == usd_pair[:3]:
            units = round(use * midle_price * action)
        else:
            units = round(use / midle_price) * action
        response = send_request(
            trade.pair, units, account_id, headers, account_type, take_profit, stop_loss
        )
        return response


def send_units_request(trade, account_type, account_id, headers):
    action = 1 if trade.action == "buy" else -1
    pipconv = Decimal(0.0001 if "JPY" not in trade.pair else 0.01)
    take_profit = trade.take_profit * pipconv
    stop_loss = trade.stop_loss * pipconv
    units = trade.units * action
    response = send_request(
        trade.pair, units, account_id, headers, account_type, take_profit, stop_loss
    )
    return response


def execute_trade(trade_id):
    try:
        trade = ScheduledTrade.objects.select_related("account").get(id=trade_id)
    except ScheduledTrade.DoesNotExist:
        return
    if not trade.account:
        trade.status = "No account"
        return
    account_type = trade.account.account_type
    oanda_token = (
        trade.account.access_token.live_token
        if account_type == "live"
        else trade.account.access_token.paper_token
    )
    headers = {
        "Authorization": f"Bearer {oanda_token}",
        "Accept-Datetime-Format": "RFC3339",
        "Content-Type": "application/json",
    }
    account_id = trade.account.account_id
    if trade.percentage:
        response = send_percentage_request(trade, account_type, account_id, headers)
    else:
        response = send_units_request(trade, account_type, account_id, headers)

    if response == -1:
        trade.status = "Failed"
        trade.save()
        return

    json_response = response.json()

    if response.status_code != 201:
        if "orderRejectTransaction" in json_response:
            trade.status = json_response["orderRejectTransaction"]["rejectReason"]
        else:
            trade.status = "Failed"
        trade.save()
        return
    if "orderCancelTransaction" in json_response:
        trade.status = json_response["orderCancelTransaction"]["reason"]
        trade.save()
        return
    trade.status = "success"
    trade.save()


def create_hook(trade_id, postAt):
    url = f"{POSTHOOK_URL}/hooks"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": POSTHOOK_API_KEY,
    }
    payload = json.dumps(
        {
            "path": "/api/trades/receive_trade/",
            "postAt": postAt.isoformat(),
            "data": {"trade_id": trade_id},
        }
    )
    response = requests.post(url, headers=headers, data=payload).json()
    return response["data"]["id"]


def validate_hook(request):
    signature = request.headers.get("X-Ph-Signature")
    if not signature:
        return False
    body = request.body
    h = hmac.new(key=signature_key.encode(), msg=body, digestmod=hashlib.sha256)
    return hmac.compare_digest(h.hexdigest(), signature)


def delete_hook(hook_id):
    url = f"{POSTHOOK_URL}/hooks/{hook_id}"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": POSTHOOK_API_KEY,
    }
    requests.delete(url, headers=headers)
