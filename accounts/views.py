from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from accounts.models import Account
from accounts.permissions import IsOwner
from accounts.serializers import AccountSerializer


@extend_schema(tags=["Accounts"])
class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsOwner]
    pagination_class = None

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
