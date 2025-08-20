from django.contrib import admin
from django.urls import path, include
from . import views
from .views import student_API



urlpatterns = [
    
    path('add/', student_API.as_view({'post':'create'})),
    path('all/', student_API.as_view({'get':'list'})),
    path('details/<int:pk>/', student_API.as_view({'get':'retrieve'})),
    path('partialupdate/<int:pk>/', student_API.as_view({'patch': 'partial_update'})),
    path('update/<int:pk>/', student_API.as_view({'put':'update'})),
    path('delete/<int:pk>/', student_API.as_view({'delete':'destroy'})),
    
     
    # path('verify_token/',views.verify_token, name='verify_token'),
    path('login/',views.login_page, name ='login_page'),
    path('register/',views.register_page, name ='register_page'),
    path('dashboard/',views.dashboard_page, name='dashboard_page'),
    # path('register_api/',views.register_function, name='register_function'),
    # path('register_api/',views.student_API.as_view({'post':'create'})),          
    # modelviewset
    # path('login_api/',views.login_function, name='login_function'),
    # path('fees-history/',views.FeeHistoryAPI.as_view({'get':'list'})),
    # path('pay-fees/',views.FeeHistoryAPI.as_view({'post':'pay_fees'})),
    path('login_api/',views.StudentLoginAPI.as_view()),                           #using modelviewset
]