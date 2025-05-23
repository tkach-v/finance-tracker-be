from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from finance_tracker import settings

urlpatterns = []

if settings.DEBUG:
    urlpatterns.extend(
        (
            path("docs/schema/", SpectacularAPIView.as_view(), name="schema"),
            path(
                "docs/",
                SpectacularSwaggerView.as_view(url_name="schema"),
                name="swagger-ui",
            ),
            path(
                "docs/redoc/",
                SpectacularRedocView.as_view(url_name="schema"),
                name="redoc",
            ),
        )
    )
