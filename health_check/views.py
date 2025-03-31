from rest_framework.response import Response
from rest_framework.views import APIView


class ApiHealthCheck(APIView):
    def get(self, request):
        result = {
            "message": "Server works",
        }
        return Response(result)
