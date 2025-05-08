from django.conf import settings
from django.db import models

from common.models import TimeStampedModel


class CategoryType(models.TextChoices):
    INCOME = "income", "Income"
    EXPENSE = "expense", "Expense"


class Category(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="categories"
    )
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=CategoryType.choices)
    color = models.CharField(
        max_length=7, default="#CCCCCC", help_text="Hex color, e.g. #FF0000"
    )
    budget_limit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Monthly budget limit in base currency (USD).",
    )

    class Meta:
        unique_together = ("user", "name", "type")
        ordering = ["type", "name"]
        verbose_name_plural = "Categories"
