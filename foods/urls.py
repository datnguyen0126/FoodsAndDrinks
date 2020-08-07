from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from foods import views
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import include
from rest_framework import routers
router = routers.DefaultRouter()

router.register('', views.RatingViewSet)

urlpatterns = [
    path('public/', views.FoodList.as_view()),
    path('', views.CreateFood.as_view()),
    path('<int:pk>/', views.FoodDetail.as_view()),
    path('rating/', include(router.urls)),
    path('categories/', views.CategoryList.as_view()),
    path('categories/<int:id>/', views.CategoryDetail.as_view()),
    path('delete_img/<int:pk>/', views.DeleteImagesInFood.as_view())
]
