from django.urls import path

from stats.views import TransactionStatsView

urlpatterns = [
    path("transactions/", TransactionStatsView.as_view(), name="transaction-stats"),
]
