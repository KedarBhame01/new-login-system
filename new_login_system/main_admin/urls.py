from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('login/',views.login_page, name ='login_page'),
    path('register/',views.register_page, name ='register_page'),
    path('register_api/',views.register_function, name='register_function'),
    path('login_api/',views.login_function, name='login_function'),
    path('dashboard/',views.dashboard_page, name='dashboard_page'),
]