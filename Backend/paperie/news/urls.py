from django.urls import path
from . import views

urlpatterns = [
    path('api/news/', views.search_news, name='search_news'),
    path('apa/news', views.apa_news, name='apa_news'),
    path('mla/news', views.mla_news, name='mla_news'),
    path('chi/news', views.chi_news, name='chi_news'),
    path('van/news', views.van_news, name='van_news'),
]