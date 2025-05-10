from django.db import models

from accounts.models import Account
from common.models import TimeStampedModel
from finance_tracker import settings


class Transaction(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions"
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="transactions",
        help_text="Account associated with the transaction",
    )
    amount = models.DecimalField(
        max_digits=30,
        decimal_places=10,
        default=0,
        help_text="Amount of the transaction",
    )
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Transactions"
