from rest_framework import routers
from .views import AuthViewSet, ProfileViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('api/auth', AuthViewSet, basename='auth')
router.register('api/user', ProfileViewSet, basename='profile')

urlpatterns = router.urls
