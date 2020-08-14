from django.urls import path
from search import views

urlpatterns = [
    path('', views.SearchList.as_view()),
]
