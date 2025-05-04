from django.db import models

from common.models import TimeStampedModel


class Currency(TimeStampedModel):
    id = models.CharField(
        max_length=255,
        unique=True,
        primary_key=True,
        help_text="Ticker code (ISO 4217 for fiat, exchange ticker for crypto, e.g. USD, EUR, BTC, ETH)",
    )
    name = models.CharField(
        max_length=255, help_text="Full currency name, e.g. 'US Dollar'"
    )
    symbol = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Currency symbol, e.g. '$', '€'; leave null if not applicable",
    )
    is_active = models.BooleanField(default=True)
    current_price = models.DecimalField(
        max_digits=20,
        decimal_places=8,
        default=0,
        null=True,
        blank=True,
        help_text="Latest price relative to base currency (USD)",
    )

    class Meta:
        verbose_name_plural = "Currencies"
        ordering = ["id"]

    def __str__(self):
        return self.name


class CurrencyPrice(models.Model):
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="prices"
    )
    date = models.DateField(help_text="Date when this price was recorded")
    price = models.DecimalField(max_digits=20, decimal_places=12)

    class Meta:
        indexes = [
            models.Index(fields=["date"], name="currency_price_date_idx"),
        ]
        ordering = ["-date"]

    def __str__(self):
        return f"{self.currency} @ {self.date}: {self.price}"
