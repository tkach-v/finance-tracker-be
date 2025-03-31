from django.contrib import admin
from django.urls import include, path

from finance_tracker.urls import develop as development_urls
from finance_tracker.urls import swagger as swagger_urls
from health_check import urls as health_check_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health-check/", include(health_check_urls)),
    path("", include(swagger_urls)),
    path("", include(development_urls)),
]
