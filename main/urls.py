from django.urls import path
from . import views
from django.shortcuts import render, redirect

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('signup/', views.signup_view, name="signup"),
    path('logout/', views.logout_view, name="logout"),
    path('new_post/', views.new_post, name="new_post"),
    path('home/', views.home, name="home"),
]