from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from health_check.serializers import HealthCheckSerializer


class ApiHealthCheck(GenericAPIView):
    serializer_class = HealthCheckSerializer

    def get(self, request):
        serializer = self.get_serializer(data={"message": "Server works"})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
