from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("finance_tracker.urls.swagger")),
    path("", include("finance_tracker.urls.develop")),
    path("api/health-check/", include("health_check.urls")),
    path("api/user/", include("users.urls")),
]
