from django.urls import path, include
from . import views

urlpatterns = [
    path('mypage', views.mypage, name='mypage'),
    path('mypage/get', views.mypage_get, name='mypage_get'),
]