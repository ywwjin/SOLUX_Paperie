from django.urls import path, include
from . import views

urlpatterns = [
    path('mypage', views.mypage, name='mypage')
]