from django.urls import path
from . import views

urlpatterns = [
    path('api/books/', views.search_books, name='search_books'),
]
