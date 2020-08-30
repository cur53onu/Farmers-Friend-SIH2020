from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.home,name='home'),
    path('basic/', views.home),
    path('signup',views.signup,name='signup'),
    path('login', views.handlelogin,name='handlelogin'),
    path('handlelogout', views.handlelogout, name='handlelogout'),
    path('Admin/', views.Admin,name='admin'),
    path('Farmer/', views.Farmer,name='farmer'),
]