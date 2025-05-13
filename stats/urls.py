from django.urls import path

from stats.views import TotalBalanceView, TransactionStatsView

urlpatterns = [
    path("transactions/", TransactionStatsView.as_view(), name="transaction-stats"),
    path("total-balance/", TotalBalanceView.as_view(), name="total-balance"),
]
