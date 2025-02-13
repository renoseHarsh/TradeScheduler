from django.contrib.auth.models import User
from rest_framework import serializers

from .models import AccessToken, Account


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]

    def create(seld, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user


class UpdateTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessToken
        fields = ["paper_token", "live_token"]


class AccessTokenSerializer(serializers.ModelSerializer):
    paper_accounts = serializers.SerializerMethodField("get_paper_accounts")
    live_accounts = serializers.SerializerMethodField("get_live_accounts")

    def get_paper_accounts(self, obj):
        return len(Account.objects.filter(access_token=obj, account_type="paper"))

    def get_live_accounts(self, obj):
        return len(Account.objects.filter(access_token=obj, account_type="live"))

    class Meta:
        model = AccessToken
        fields = [
            "paper_token",
            "live_token",
            "paper_accounts",
            "live_accounts",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]
