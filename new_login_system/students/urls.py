# Add these URL patterns to your students/urls.py

from django.contrib import admin
from django.urls import path, include
from . import views
from .views import student_API, StudentLoginAPI

urlpatterns = [
    # API endpoints (existing)
    path('add/', student_API.as_view({'post':'create'})),
    path('all/', student_API.as_view({'get':'list'})),
    path('details/<int:pk>/', student_API.as_view({'get':'retrieve'})),
    path('partialupdate/<int:pk>/', student_API.as_view({'patch': 'partial_update'})),
    path('update/<int:pk>/', student_API.as_view({'put':'update'})),
    path('delete/<int:pk>/', student_API.as_view({'delete':'destroy'})),
    path('login_api/', StudentLoginAPI.as_view({'post':'login'})),
    path('search/', student_API.as_view({'post':'search'})),
    
    # Web pages (new)
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
    path('dashboard/', views.dashboard_page, name='dashboard_page'),
    path('profile/', views.profile_page, name='profile_page'),
    path('fees/', views.fees_page, name='fees_page'),
    path('attendance/', views.attendance_page, name='attendance_page'),
    path('homework/', views.homework_page, name='homework_page'),
    path('notices/', views.notices_page, name='notices_page'),
]