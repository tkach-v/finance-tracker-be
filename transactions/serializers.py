from rest_framework import serializers

from transactions.models import Transaction


class TransactionsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Transaction
        fields = (
            "id",
            "user",
            "account",
            "amount",
            "description",
            "date",
            "category",
            "type",
        )
        read_only_fields = ("id",)
