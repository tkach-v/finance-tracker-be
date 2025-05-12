from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from transactions.models import Transaction
from transactions.permissions import IsOwner
from transactions.serializers import TransactionsSerializer


@extend_schema(tags=["Transactions"])
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionsSerializer
    permission_classes = [IsOwner]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category", "account", "type"]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
