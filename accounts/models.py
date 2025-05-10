from django.conf import settings
from django.db import models

from common.models import TimeStampedModel


class Account(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="accounts"
    )
    name = models.CharField(max_length=255)
    color = models.CharField(
        max_length=7, default="#CCCCCC", help_text="Hex color, e.g. #FF0000"
    )

    class Meta:
        unique_together = ("user", "name")
        ordering = ["name"]
        verbose_name_plural = "Accounts"
