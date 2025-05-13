from datetime import datetime, timedelta

from django.db.models import (
    Case,
    DecimalField,
    ExpressionWrapper,
    F,
    OuterRef,
    Q,
    Subquery,
    Sum,
    When,
)
from django.db.models.functions import (
    Coalesce,
    TruncDay,
    TruncMonth,
    TruncWeek,
    TruncYear,
)
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account
from currencies.models import CurrencyPrice
from transactions.models import Transaction


@extend_schema(tags=["Statistics"])
class TransactionStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Returns aggregated transaction statistics for a user for the last year.
        Query parameters:
        - account_ids: Comma-separated list of account IDs to filter by.
        - start_date: Start date for the statistics (YYYY-MM-DD).
        - end_date: End date for the statistics (YYYY-MM-DD).
        - freq: Frequency of the statistics (daily, weekly, monthly, yearly).
        """
        user = request.user
        params = request.query_params

        account_ids = params.get("account_ids")
        if account_ids:
            account_ids = [int(pk) for pk in account_ids.split(",")]

        end_date = params.get("end_date")
        start_date = params.get("start_date")
        today = datetime.today().date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else today
        start = (
            datetime.strptime(start_date, "%Y-%m-%d").date()
            if start_date
            else end - timedelta(days=365 * 100)
        )

        freq = params.get("freq", "monthly")
        trunc_map = {
            "daily": TruncDay,
            "weekly": TruncWeek,
            "monthly": TruncMonth,
            "yearly": TruncYear,
        }
        TruncFunc = trunc_map.get(freq, TruncMonth)

        price_qs = (
            CurrencyPrice.objects.filter(
                currency_id=OuterRef("account__currency_id"), date__lte=OuterRef("date")
            )
            .order_by("-date")
            .values("price")[:1]
        )

        # Annotate each transaction with usd_amount = amount * price or current_price
        usd_expr = ExpressionWrapper(
            F("amount")
            * Coalesce(Subquery(price_qs), F("account__currency__current_price")),
            output_field=DecimalField(max_digits=20, decimal_places=2),
        )

        qs = Transaction.objects.filter(user=user)
        if start_date:
            qs = qs.filter(date__gte=start)
        if end_date:
            qs = qs.filter(date__lte=end)
        if account_ids:
            qs = qs.filter(account_id__in=account_ids)

        qs = (
            qs.annotate(period=TruncFunc("date"))
            .annotate(usd_amount=usd_expr)
            .values("period")
            .annotate(
                income_usd=Sum("usd_amount", filter=Q(type="income")),
                expense_usd=Sum("usd_amount", filter=Q(type="expense")),
            )
            .order_by("period")
        )

        fmt = {
            "daily": "%Y-%m-%d",
            "weekly": "%Y-%W",
            "monthly": "%Y-%m",
            "yearly": "%Y",
        }[freq]
        data = [
            {
                "period": entry["period"].strftime(fmt),
                "income": float(entry["income_usd"] or 0),
                "expense": float(entry["expense_usd"] or 0),
            }
            for entry in qs
        ]
        return Response(data)


@extend_schema(tags=["Statistics"])
class TotalBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        accounts_qs = Account.objects.filter(user=user).annotate(
            local_balance=Sum(
                Case(
                    When(transactions__type="income", then=F("transactions__amount")),
                    When(
                        transactions__type="expense",
                        then=F("transactions__amount") * -1,
                    ),
                    output_field=DecimalField(max_digits=20, decimal_places=2),
                )
            )
        )

        price_qs = (
            CurrencyPrice.objects.filter(
                currency_id=OuterRef("currency_id"), date__lte=datetime.today().date()
            )
            .order_by("-date")
            .values("price")[:1]
        )

        accounts_usd = accounts_qs.annotate(
            rate=Coalesce(Subquery(price_qs), F("currency__current_price")),
            balance_usd=ExpressionWrapper(
                F("local_balance") * F("rate"),
                output_field=DecimalField(max_digits=20, decimal_places=2),
            ),
        ).aggregate(total_usd=Sum("balance_usd"))

        total = accounts_usd.get("total_usd") or 0
        return Response({"total_usd": float(total)})
