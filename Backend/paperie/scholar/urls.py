from django.urls import path
from . import views

urlpatterns = [
    path('api/scholar', views.search_scholar, name='search_scholar'),
]
