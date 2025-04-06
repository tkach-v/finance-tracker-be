from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from users.serializers import UserSerializer


@extend_schema(tags=["User"])
class UserViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""

    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def get_queryset(self):
        """Retrieve users by created_at field."""
        return self.queryset.order_by("created_at")
