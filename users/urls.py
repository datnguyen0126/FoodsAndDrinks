from rest_framework import routers
from .views import AuthViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('api', AuthViewSet, basename='user')

urlpatterns = router.urls
