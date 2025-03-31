from rest_framework import serializers


class HealthCheckSerializer(serializers.Serializer):
    message = serializers.CharField()
