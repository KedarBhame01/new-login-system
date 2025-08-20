from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import student_API, FeeHistoryAPI

router = DefaultRouter()
router.register(r'student_api', views.student_API, basename='student_api')

router1 = DefaultRouter()
router1.register(r'FeeHistoryAPI', views.FeeHistoryAPI, basename='FeeHistoryAPI')

urlpatterns = [
    #  path('student/',include(router.urls)),
    #  path('feehistoryapi/',include(router1.urls)),
     
    path('student/add/', student_API.as_view({'post':'create'})),
    path('student/all/', student_API.as_view({'get':'list'})),
    path('student/details/<int:pk>/', student_API.as_view({'get':'retrieve'})),
        path('student/partialupdate/<int:pk>/', student_API.as_view({'patch': 'partial_update'})),
    path('student/update/<int:pk>/', student_API.as_view({'put':'update'})),
    path('student/delete/<int:pk>/', student_API.as_view({'delete':'destroy'})),
    
    path('fees/pay/', FeeHistoryAPI.as_view({'post':'pay_fees'})),
    path('fees/add/', FeeHistoryAPI.as_view({'post':'create'})),
    # path('fees/nadd/', FeeHistoryAPI.as_view({'post':'ncreate'})),
    path('fees/all/', FeeHistoryAPI.as_view({'get':'list'})),
    path('fees/details/<int:pk>/', FeeHistoryAPI.as_view({'get':'retrieve'})),
    path('fees/partialupdate/<int:pk>/', FeeHistoryAPI.as_view({'patch': 'partial_update'})),
    path('fees/update/<int:pk>/', FeeHistoryAPI.as_view({'put':'update'})),
    path('fees/delete/<int:pk>/', FeeHistoryAPI.as_view({'delete':'destroy'})),
     
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