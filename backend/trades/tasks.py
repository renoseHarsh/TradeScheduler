from celery import shared_task

from .models import ScheduledTrade
from .utils import send_percentage_request, send_units_request


@shared_task
def execute_trade(trade_id):
    try:
        trade = ScheduledTrade.objects.select_related("account").get(id=trade_id)
    except ScheduledTrade.DoesNotExist:
        return
    if not trade.account:
        trade.status = "No account"
        trade.save()
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
