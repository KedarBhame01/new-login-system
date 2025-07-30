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
    path('attendance/add/', AttendanceViewset.as_view({'post':'create'})),
    path('attendance/all/', AttendanceViewset.as_view({'get':'list'})),
    path('attendance/by-date/', AttendanceViewset.as_view({'post':'by_date'})),
    path('attendance/details/<int:pk>/', AttendanceViewset.as_view({'get':'retrieve'})),
    path('attendance/update/<int:pk>/', AttendanceViewset.as_view({'put':'update'})),
    path('attendance/delete/<int:pk>/', AttendanceViewset.as_view({'delete':'destroy'})),

    path('notice/add/', NoticeViewSet.as_view({'post':'create'})),
    path('notice/all/', NoticeViewSet.as_view({'get':'list'})),
    path('notice/details/<int:pk>/', NoticeViewSet.as_view({'get':'retrieve'})),
    path('notice/update/<int:pk>/', NoticeViewSet.as_view({'put':'update'})),
    path('notice/delete/<int:pk>/', NoticeViewSet.as_view({'delete':'destroy'})),

    path('admin/add/',AdminViewSet.as_view({'post':'create'})), 
    # path('all_notice/',NoticeViewSet.as_view({'get':'list'})),

]