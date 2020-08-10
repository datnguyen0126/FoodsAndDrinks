from django.urls import path
from . import views

urlpatterns = [
    path('<int:food_id>', views.CommentList.as_view()),
    path('<int:id>/', views.CommentDetail.as_view()),
]
