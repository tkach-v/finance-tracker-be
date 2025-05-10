from django.conf import settings
from django.db import models

from common.models import TimeStampedModel
from currencies.models import Currency


class Account(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="accounts"
    )
    name = models.CharField(max_length=255)
    color = models.CharField(
        max_length=7, default="#CCCCCC", help_text="Hex color, e.g. #FF0000"
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name="accounts",
        help_text="Currency of the account",
    )
    balance = models.DecimalField(
        max_digits=30,
        decimal_places=10,
        default=0,
        help_text="Current balance in the account",
    )

    class Meta:
        unique_together = ("user", "name")
        ordering = ["name"]
        verbose_name_plural = "Accounts"
