from django.urls import path
from . import views
from django.shortcuts import render, redirect

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('signup/', views.signup_view, name="signup"),
    path('logout/', views.logout_view, name="logout"),
    path('new_post/', views.new_post, name="new_post"),
    path('home/', views.home, name="home"),
    path('my_posts/', views.my_posts, name="my_posts"),
    path('category_page/<str:current_category>/', views.category_page, name="category_page"),
    path('post_detail/<int:primary_key>/', views.post_detail, name="post_detail"),
    path('edit_post/<int:primary_key>/', views.edit_post, name="edit_post"),
]