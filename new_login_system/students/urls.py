from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'student_api', views.student_API, basename='student_api')

urlpatterns = [
     path('student/',include(router.urls)),
    # path('verify_token/',views.verify_token, name='verify_token'),
    path('login/',views.login_page, name ='login_page'),
    path('register/',views.register_page, name ='register_page'),
    # path('register_api/',views.register_function, name='register_function'),
    path('register_api/',views.student_API.as_view({'post':'create'})),           #using modelviewset
    # path('login_api/',views.login_function, name='login_function'),
    path('login_api/',views.StudentLoginAPI.as_view()),                           #using modelviewset
    path('dashboard/',views.dashboard_page, name='dashboard_page'),
]