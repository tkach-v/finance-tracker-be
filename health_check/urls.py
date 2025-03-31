from django.urls import path

from health_check.views import ApiHealthCheck

urlpatterns = [
    path('', ApiHealthCheck.as_view()),
]
