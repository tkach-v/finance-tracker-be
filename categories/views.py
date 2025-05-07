from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from categories.models import Category
from categories.permissions import IsOwner
from categories.serializers import CategorySerializer


@extend_schema(tags=["Cagegories"])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsOwner]
    pagination_class = None

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
