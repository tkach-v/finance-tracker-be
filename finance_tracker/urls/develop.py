from django.urls import include, path

from finance_tracker import settings

urlpatterns = []

if settings.DEBUG:
    if settings.PROFILERS_ENABLED:
        urlpatterns.append(path("silk/", include("silk.urls", namespace="silk")))
