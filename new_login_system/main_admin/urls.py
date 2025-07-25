from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoticeViewSet,Admin_API
# from . import views
router = DefaultRouter()
router.register(r'notices', NoticeViewSet, basename='notice')

urlpatterns = [
    path('',include(router.urls)),
    path('register_api/',Admin_API.as_view({'post':'create'})), 
    path('show_notices/',Admin_API.as_view({'get':'list'})),
#     path('login/',views.login_page, name ='login_page'),
#     path('register/',views.register_page, name ='register_page'),
#     # path('register_api/',views.register_function, name='register_function'),
#     path('register_api/',views.student_API.as_view({'post':'create'})),           #using modelviewset
#     # path('login_api/',views.login_function, name='login_function'),
#     path('login_api/',views.StudentLoginAPI.as_view()),                           #using modelviewset
#     path('dashboard/',views.dashboard_page, name='dashboard_page'),
]