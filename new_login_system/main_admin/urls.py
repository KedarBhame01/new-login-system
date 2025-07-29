from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoticeViewSet,AdminViewSet, AttendanceViewset
# from . import views
router = DefaultRouter()
router.register(r'notices', NoticeViewSet, basename='notice')
router1 = DefaultRouter()
router1.register(r'attendance', AttendanceViewset, basename='attendance')

urlpatterns = [
    # path('notices/',include(router.urls)),
    # path('attendance/', include(router1.urls)),
    path('attendance/', AttendanceViewset.as_view({'get':'list'})),
    path('attendance', AttendanceViewset.as_view({'post':'create'})),
    path('register_api/',AdminViewSet.as_view({'post':'create'})), 
    path('show_notices/',NoticeViewSet.as_view({'get':'list'})),

]