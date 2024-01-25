from django.urls import path
from . import views

urlpatterns = [
    path('api/scholars', views.search_scholars, name='search_scholars'),
    path('apa/scholars', views.apa_scholars, name='apa_scholars'),
    path('mla/scholars', views.mla_scholars, name='mla_scholars'),
    path('chi/scholars', views.chi_scholars, name='chi_scholars'),
    path('van/scholars', views.van_scholars, name='van_scholars'),
]