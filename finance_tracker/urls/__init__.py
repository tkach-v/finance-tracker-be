from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("finance_tracker.urls.swagger")),
    path("", include("finance_tracker.urls.develop")),
    path("api/health-check/", include("health_check.urls")),
    path("api/", include("djoser.urls")),
    path("api/", include("djoser.urls.jwt")),
    path("api/currencies/", include("currencies.urls")),
    path("api/categories/", include("categories.urls")),
]
