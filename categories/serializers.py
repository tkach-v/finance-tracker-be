from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = ("id", "user", "name", "type", "color", "budget_limit")
        read_only_fields = ("id",)
        validators = [
            UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=["user", "name", "type"],
                message="You already have a category with that name and type.",
            )
        ]
