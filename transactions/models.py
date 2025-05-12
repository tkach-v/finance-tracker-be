from django.db import models, transaction
from django.db.models import F

from accounts.models import Account
from categories.models import Category
from common.models import TimeStampedModel
from finance_tracker import settings


class TransactionType(models.TextChoices):
    INCOME = "income", "Income"
    EXPENSE = "expense", "Expense"


class Transaction(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions"
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="transactions",
        help_text="Account associated with the transaction",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="transactions",
        help_text="Category of the transaction",
    )
    amount = models.DecimalField(
        max_digits=30,
        decimal_places=10,
        default=0,
        help_text="Amount of the transaction",
    )
    description = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=10, choices=TransactionType.choices)
    date = models.DateField(help_text="Date of the transaction")

    class Meta:
        ordering = ["-date", "-created_at"]
        verbose_name_plural = "Transactions"

    def save(self, *args, **kwargs):
        # when creating or updating, change account balance
        if self._state.adding:
            delta = self.amount if self.type == TransactionType.INCOME else -self.amount
        else:
            old = Transaction.objects.get(pk=self.pk)
            old_delta = (
                old.amount if old.type == TransactionType.INCOME else -old.amount
            )
            new_delta = (
                self.amount if self.type == TransactionType.INCOME else -self.amount
            )
            delta = new_delta - old_delta

        super().save(*args, **kwargs)

        if delta:
            with transaction.atomic():
                Account.objects.filter(pk=self.account.pk).update(
                    balance=F("balance") + delta
                )

    def delete(self, *args, **kwargs):
        # when deleting, revert original effect on account balance
        delta = -self.amount if self.type == TransactionType.INCOME else self.amount
        with transaction.atomic():
            Account.objects.filter(pk=self.account.pk).update(
                balance=F("balance") + delta
            )
            super().delete(*args, **kwargs)
