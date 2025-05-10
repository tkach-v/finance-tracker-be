from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Account
        fields = ("id", "user", "name", "color", "currency", "balance")
        read_only_fields = ("id",)
        validators = [
            UniqueTogetherValidator(
                queryset=Account.objects.all(),
                fields=["user", "name"],
                message="You already have an account with that name.",
            )
        ]
