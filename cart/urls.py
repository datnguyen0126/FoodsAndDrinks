from rest_framework import routers
from .views import CartViewSet

app_name = 'cart'

router = routers.DefaultRouter(trailing_slash=False)
router.register('', CartViewSet, basename='cart')

urlpatterns = router.urls

