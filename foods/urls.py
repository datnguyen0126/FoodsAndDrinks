from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from foods import views

urlpatterns = [
    path('public/', views.FoodList.as_view()),
    path('', views.CreateFood.as_view()),
    path('<int:pk>/', views.FoodDetail.as_view()),
    path('delete_img/<int:pk>/', views.DeleteImagesInFood.as_view())
]
