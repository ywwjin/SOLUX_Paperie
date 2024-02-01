"""
URL configuration for paperie project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from book.views import search_books, apa_books, mla_books, chi_books, van_books
from news.views import search_news, apa_news, mla_news, chi_news, van_news
from scholar.views import search_scholars, apa_scholars, mla_scholars, chi_scholars, van_scholars
from mypage.views import mypage_get, mypage_books, mypage_news, mypage_scholars

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),

    path('api/books', search_books, name='search_books'),
    path('api/news', search_news, name='search_news'),
    path('api/scholars', search_scholars, name='search_scholars'),

    path('apa/books', apa_books, name='apa_books'),
    path('mla/books', mla_books, name='mla_books'),
    path('chi/books', chi_books, name='chi_books'),
    path('van/books', van_books, name='van_books'),

    path('apa/news', apa_news, name='apa_news'),
    path('mla/news', mla_news, name='mla_news'),
    path('chi/news', chi_news, name='chi_news'),
    path('van/news', van_news, name='van_news'),

    path('apa/scholars', apa_scholars, name='apa_scholars'),
    path('mla/scholars', mla_scholars, name='mla_scholars'),
    path('chi/scholars', chi_scholars, name='chi_scholars'),
    path('van/scholars', van_scholars, name='van_scholars'),

    path('mypage/get', mypage_get, name='mypage_get'),
    path('mypage/books', mypage_books, name='mypage_books'),
    path('mypage/news', mypage_news, name='mypage_news'),
    path('mypage/scholars', mypage_scholars, name='mypage_scholars'),
]