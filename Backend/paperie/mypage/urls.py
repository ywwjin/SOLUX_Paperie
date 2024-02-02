from django.urls import path, include
from . import views

urlpatterns = [
    path('mypage/save', views.mypage_save, name='mypage_save'),
    path('mypage/all', views.mypage_all, name='mypage_all'),
]