from rest_framework import routers
from .views import OrderViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('', OrderViewSet, basename='order')

urlpatterns = router.urls

