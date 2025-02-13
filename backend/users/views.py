from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import AccessToken, Account
from .serializers import (
    AccessTokenSerializer,
    RegisterSerializer,
    UpdateTokenSerializer,
    UserSerializer,
)
from .utils import get_account_ids


# Create your views here.
@api_view(["POST"])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        login(request, serializer.instance)
        return Response(
            {"message": "success", "data": UserSerializer(serializer.instance).data},
            status=201,
        )
    if "username" in serializer.errors:
        return Response({"message": serializer.errors["username"][0]}, status=400)
    if "password" in serializer.errors:
        return Response({"message": serializer.errors["password"][0]}, status=400)
    return Response({"message": "Invalid data"}, status=400)


@api_view(["POST"])
def login_user(request):
    if not request.data.get("username") or not request.data.get("password"):
        return Response(
            {"message": "Username and password are required."},
            status=400,
        )
    user = authenticate(
        username=request.data["username"], password=request.data["password"]
    )
    if not user:
        return Response({"message": "Wrong Username or Password"}, status=400)
    login(request, user)
    return Response(
        {"message": "success", "data": UserSerializer(user).data}, status=200
    )


@api_view(["POST"])
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return Response({"message": "success"}, status=200)
    return Response({"message": "Not authorised"}, status=403)


@api_view(["GET"])
def get_user(request):
    if request.user.is_authenticated:
        return Response(
            {"message": "success", "data": UserSerializer(request.user).data},
            status=200,
        )
    return Response({"message": "Not authorised"}, status=403)


@api_view(["PUT"])
def update_tokens(request):
    if not request.user.is_authenticated:
        return Response({"message": "Not authorised"}, status=403)
    tokens = request.user.accesstoken
    if not tokens:
        return Response({"message": "Server Error"}, status=500)

    if "paper_token" in request.data:
        new_paper_accounts = get_account_ids(request.data["paper_token"])
        if request.data["paper_token"] == "" or new_paper_accounts:
            tokens.paper_token = request.data["paper_token"]
            Account.objects.filter(access_token=tokens, account_type="paper").delete()
            for account in new_paper_accounts:
                Account.objects.create(
                    access_token=tokens, account_id=account["id"], account_type="paper"
                )
        else:
            return Response({"message": "Invalid Paper Token"}, status=400)
    if "live_token" in request.data:
        new_live_accounts = get_account_ids(request.data["live_token"], True)
        if request.data["live_token"] == "" or new_live_accounts:
            tokens.live_token = request.data["live_token"]
            Account.objects.filter(access_token=tokens, account_type="live").delete()
            for account in new_live_accounts:
                Account.objects.create(
                    access_token=tokens, account_id=account["id"], account_type="live"
                )
        else:
            return Response({"message": "Invalid Live Token"}, status=400)
    tokens.save()
    data = {
        "paper_token": tokens.paper_token,
        "live_token": tokens.live_token,
        "paper_accounts": Account.objects.filter(
            account_type="paper", access_token=tokens
        ).count(),
        "live_accounts": Account.objects.filter(
            account_type="live", access_token=tokens
        ).count(),
    }
    return Response({"message": "success", "data": data}, status=200)


@api_view(["GET"])
def get_tokens(request):
    if not request.user.is_authenticated:
        return Response({"message": "Not authorised"}, status=403)
    tokens = request.user.accesstoken
    if not tokens:
        return Response({"message": "Server Error"}, status=500)

    data = {
        "paper_token": tokens.paper_token,
        "live_token": tokens.live_token,
        "paper_accounts": Account.objects.filter(
            account_type="paper", access_token=tokens
        ).count(),
        "live_accounts": Account.objects.filter(
            account_type="live", access_token=tokens
        ).count(),
    }

    return Response({"message": "success", "data": data}, status=200)


@api_view(["GET"])
def get_accounts(request):
    if not request.user.is_authenticated:
        return Response({"message": "Not authorised"}, status=403)
    tokens = request.user.accesstoken
    if not tokens:
        return Response({"message": "Server Error"}, status=500)

    data = {
        "paper_accounts": Account.objects.filter(
            account_type="paper", access_token=tokens
        ).values_list("account_id", flat=True),
        "live_accounts": Account.objects.filter(
            account_type="live", access_token=tokens
        ).values_list("account_id", flat=True),
    }

    return Response({"message": "success", "data": data}, status=200)
