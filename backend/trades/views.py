from celery.result import AsyncResult
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import Account

from .models import ScheduledTrade
from .serializers import ScheduledTradeSerializer, ScheduleTradeSerializer

# Create your views here.

load_dotenv()


@api_view(["POST"])
def schedule(request):
    if not request.user.is_authenticated:
        return Response({"message": "Unauthorised"}, status=401)
    serializer = ScheduleTradeSerializer(data=request.data)
    if serializer.is_valid():
        try:
            account = request.user.accesstoken.account_set.get(
                account_id=request.data["account_id"]
            )
        except Account.DoesNotExist:
            return Response({"message": "Not Found"}, status=404)
        scheduled_time = serializer.validated_data.get("scheduled_time")
        if scheduled_time and scheduled_time <= timezone.now():
            return Response({"message": "Time needs to be in future"}, status=400)

        serializer.save(user=request.user, account=account)
        return Response({"message": "OK"}, status=201)
    return Response({"message": "Bad Request"}, status=400)


@api_view(["GET"])
def get_scheduled(request):
    if not request.user.is_authenticated:
        return Response({"message": "Unauthorised"}, status=401)
    trades = (
        ScheduledTrade.objects.filter(user=request.user)
        .select_related("account")
        .order_by("-scheduled_time")
    )
    serializer = ScheduledTradeSerializer(trades, many=True)
    return Response({"message": "OK", "data": serializer.data}, status=200)

@api_view(["PUT"])
def update_scheduled(request):
    if not request.user.is_authenticated:
        return Response({"message": "Unauthorised"}, status=401)
    try:
        og_trade = ScheduledTrade.objects.select_related("account").get(
            id=request.data["id"], user=request.user
        )
    except ScheduledTrade.DoesNotExist:
        return Response({"message": "Not Found"}, status=404)

    if "percentage" in request.data and request.data["percentage"] is not None:
        request.data["units"] = None
    elif "units" in request.data and request.data["units"] is not None:
        request.data["percentage"] = None

    if og_trade.account.account_id != request.data["account_id"]:
        try:
            account = request.user.accesstoken.account_set.get(
                account_id=request.data["account_id"]
            )
        except Account.DoesNotExist:
            return Response({"message": "Not Found"}, status=404)
        og_trade.account = account

    og_time = og_trade.scheduled_time
    serializer = ScheduleTradeSerializer(og_trade, data=request.data)
    if serializer.is_valid():
        if og_time != serializer.validated_data.get("scheduled_time"):
            AsyncResult(og_trade.task_id).revoke(terminate=True)
            # delete_hook(og_trade.posthook_id)
            # new_hook_id = create_hook(
            #     og_trade.id, serializer.validated_data.get("scheduled_time")
            # )
            serializer.instance.task_id = None
        print(serializer)
        serializer.save()
        return Response({"message": "OK"}, status=200)
    return Response({"message": "Bad Request"}, status=400)


@api_view(["DELETE"])
def delete_scheduled(request, pk):
    if not request.user.is_authenticated:
        return Response({"message": "Unauthorised"}, status=401)
    try:
        trade = ScheduledTrade.objects.get(id=pk, user=request.user)
    except ScheduledTrade.DoesNotExist:
        return Response({"message": "Not Found"}, status=404)
    AsyncResult(trade.task_id).revoke(terminate=True)
    trade.delete()
    return Response({"message": "OK"}, status=200)
