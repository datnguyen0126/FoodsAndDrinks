from rest_framework import routers
from django.urls import path
from .views import AuthViewSet, PasswordViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('api', AuthViewSet, basename='user')
router.register('api/user', PasswordViewSet, basename='password')

urlpatterns = router.urls

