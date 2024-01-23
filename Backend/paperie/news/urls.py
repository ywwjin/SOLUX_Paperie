from django.urls import path
from . import views

urlpatterns = [
    path('api/news/', views.search_news, name='search_news'),
]