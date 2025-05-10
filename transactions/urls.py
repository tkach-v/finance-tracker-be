from rest_framework.routers import DefaultRouter

from transactions.views import TransactionViewSet

router = DefaultRouter()
router.register("", TransactionViewSet, basename="transaction")

urlpatterns = router.urls
