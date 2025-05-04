import datetime

from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from currencies.models import Currency, CurrencyPrice
from currencies.serializers import CurrencySerializer


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
