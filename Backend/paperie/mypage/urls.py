from django.urls import path, include
from . import views

urlpatterns = [
    path('mypage', views.mypage, name='mypage'),
    path('mypage/get', views.mypage_get, name='mypage_get'),
    path('mypage/books', views.mypage_books, name='mypage_books'),
    path('mypage/news', views.mypage_news, name='mypage_news'),
    path('mypage/scholars', views.mypage_scholars, name='mypage_scholars'),
]