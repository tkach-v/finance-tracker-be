from rest_framework.routers import DefaultRouter

from currencies.views import CurrencyViewSet

router = DefaultRouter()
router.register("", CurrencyViewSet, basename="currency")

urlpatterns = router.urls
