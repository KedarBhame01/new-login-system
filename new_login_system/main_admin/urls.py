from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoticeViewSet,AdminViewSet, AttendanceViewset, CalenderViewSet, HomeworkViewSet
from django.conf import settings
from django.conf.urls.static import static
# from . import views
# router = DefaultRouter()
# router.register(r'notices', NoticeViewSet, basename='notice')
# router1 = DefaultRouter()
# router1.register(r'attendance', AttendanceViewset, basename='attendance')
router2 = DefaultRouter()
router2.register(r'calender', CalenderViewSet, basename='calender')
router3 = DefaultRouter()
router3.register(r'Homework', HomeworkViewSet, basename='Homework')
urlpatterns = [
    # path('notices/',include(router.urls)),
    # path('attendance/', include(router1.urls)),
    # path('calender', include(router2.urls)),
    # path('homework', include(router3.urls)),
    path('attendance/add/', AttendanceViewset.as_view({'post':'create'})),
    path('attendance/all/', AttendanceViewset.as_view({'get':'list'})),
    path('attendance/details/<int:pk>/', AttendanceViewset.as_view({'get':'retrieve'})),
    path('attendance/update/<int:pk>/', AttendanceViewset.as_view({'put':'update'})),
    path('attendance/delete/<int:pk>/', AttendanceViewset.as_view({'delete':'destroy'})),
    path('attendance/by-date/', AttendanceViewset.as_view({'post':'by_date'})),
    path('attendance/summery/', AttendanceViewset.as_view({'post':'attendance_summary'})),
    
    path('calender/add/', CalenderViewSet.as_view({'post':'create'})),
    path('calender/all/', CalenderViewSet.as_view({'get':'list'})),
    path('calender/details/<int:pk>/', CalenderViewSet.as_view({'get':'retrieve'})),
    path('calender/update/<int:pk>/', CalenderViewSet.as_view({'put':'update'})),
    path('calender/delete/<int:pk>/', CalenderViewSet.as_view({'delete':'destroy'})),
    
    path('homework/add/', HomeworkViewSet.as_view({'post':'create'})),
    path('homework/all/', HomeworkViewSet.as_view({'get':'list'})),
    path('homework/details/<int:pk>/', HomeworkViewSet.as_view({'get':'retrieve'})),
    path('homework/update/<int:pk>/', HomeworkViewSet.as_view({'put':'update'})),
    path('homework/delete/<int:pk>/', HomeworkViewSet.as_view({'delete':'destroy'})),
    
    path('notice/add/', NoticeViewSet.as_view({'post':'create'})),
    path('notice/all/', NoticeViewSet.as_view({'get':'list'})),
    path('notice/details/<int:pk>/', NoticeViewSet.as_view({'get':'retrieve'})),
    path('notice/update/<int:pk>/', NoticeViewSet.as_view({'put':'update'})),
    path('notice/delete/<int:pk>/', NoticeViewSet.as_view({'delete':'destroy'})),

    path('admin/add/',AdminViewSet.as_view({'post':'create'})),
    path('admin/all/', AdminViewSet.as_view({'get':'list'})),
    path('admin/details/<int:pk>/', AdminViewSet.as_view({'get':'retrieve'})),
    path('admin/partialupdate/<int:pk>/', AdminViewSet.as_view({'patch': 'partial_update'})),
    path('admin/update/<int:pk>/', AdminViewSet.as_view({'put':'update'})),
    path('admin/delete/<int:pk>/', AdminViewSet.as_view({'delete':'destroy'})), 
    # path('all_notice/',NoticeViewSet.as_view({'get':'list'})),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)