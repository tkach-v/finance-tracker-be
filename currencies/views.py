import datetime

from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from currencies.models import Currency, CurrencyPrice, CurrencyType
from currencies.serializers import CurrencySerializer
from finance_tracker.scripts.get_coingecko_currencies import (
    fetch_top_cryptos,
    fetch_top_fiats,
)


@extend_schema(tags=["Currencies"])
class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    lookup_field = "id"
    pagination_class = None

    @action(detail=True, methods=["get"], url_path="price")
    def price(self, request, id=None):
        """
        Return the historical price of this currency for a given date.
        Query parameter: ?date=YYYY-MM-DD
        """
        date_str = request.query_params.get("date")
        if not date_str:
            return Response(
                {"detail": "Query param 'date' is required (YYYY-MM-DD)"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            date = datetime.datetime.fromisoformat(date_str).date()
        except ValueError:
            return Response(
                {"detail": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        currency = self.get_object()
        price_obj = CurrencyPrice.objects.filter(currency=currency, date=date).first()
        if not price_obj:
            return Response(
                {"detail": "Price not found for this date."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {
                "currency": currency.id,
                "date": price_obj.date,
                "price": price_obj.price,
            }
        )

    @extend_schema(request=None)
    @action(
        detail=False,
        methods=["post"],
        url_path="populate",
        permission_classes=[IsAdminUser],
    )
    def populate(self, request):
        """
        Admin endpoint to populate the database with currencies.
        This will create/update the top 200 cryptocurrencies and fiat currencies.
        It will set the current price and create today's history in CurrencyPrice for cryptocurrencies.
        """

        cryptos = fetch_top_cryptos()

        for item in cryptos:
            cur, _ = Currency.objects.update_or_create(
                id=item["id"],
                defaults={
                    "name": item["name"],
                    "symbol": item["symbol"],
                    "current_price": item["price_usd"],
                    "type": CurrencyType.CRYPTO,
                },
            )
            CurrencyPrice.objects.create(
                currency=cur, date=timezone.now().date(), price=item["price_usd"]
            )

        fiats = fetch_top_fiats()
        for item in fiats:
            cur, _ = Currency.objects.update_or_create(
                id=item["code"].lower(),
                defaults={
                    "name": item["code"],
                    "symbol": item["symbol"],
                    "current_price": item["price_usd"],
                    "type": CurrencyType.FIAT,
                },
            )
            CurrencyPrice.objects.create(
                currency=cur,
                date=timezone.now().date(),
                price=item["price_usd"],
            )

        return Response(
            {
                "cryptocurrencies": len(cryptos),
                "fiat_currencies": len(fiats),
            },
            status=status.HTTP_201_CREATED,
        )
