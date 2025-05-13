from datetime import datetime, timedelta

from django.db.models import Q, Sum
from django.db.models.functions import TruncDay, TruncMonth, TruncWeek, TruncYear
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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

        qs = Transaction.objects.filter(user=user)
        if start_date:
            qs = qs.filter(date__gte=start)
        if end_date:
            qs = qs.filter(date__lte=end)
        if account_ids:
            qs = qs.filter(account_id__in=account_ids)

        qs = (
            qs.annotate(period=TruncFunc("date"))
            .values("period")
            .annotate(
                income=Sum("amount", filter=Q(type="income")),
                expense=Sum("amount", filter=Q(type="expense")),
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
                "income": float(entry["income"] or 0),
                "expense": float(entry["expense"] or 0),
            }
            for entry in qs
        ]
        return Response(data)
