from django.urls import path
from . import views
from django.shortcuts import render, redirect

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('home/', views.home, name="home"),
]