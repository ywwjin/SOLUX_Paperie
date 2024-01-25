from django.urls import path
from . import views

urlpatterns = [
    path('api/books', views.search_books, name='search_books'),
    path('apa/books', views.apa_books, name='apa_books'),
    path('mla/books', views.mla_books, name='mla_books'),
    path('chi/books', views.chi_books, name='chi_books'),
    path('van/books', views.van_books, name='van_books'),
]
