from django.contrib import admin
from django.urls import path
from .views import NoticeViewSet,AdminViewSet, CalenderViewSet, HomeworkViewSet
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('calender/add/', CalenderViewSet.as_view({'post':'create'})),
    path('calender/all/', CalenderViewSet.as_view({'get':'list'})),
    path('calender/details/<int:pk>/', CalenderViewSet.as_view({'get':'retrieve'})),
    path('calender/partialupdate/<int:pk>/', CalenderViewSet.as_view({'patch': 'partial_update'})),
    path('calender/update/<int:pk>/', CalenderViewSet.as_view({'put':'update'})),
    path('calender/delete/<int:pk>/', CalenderViewSet.as_view({'delete':'destroy'})),
    
    path('homework/add/', HomeworkViewSet.as_view({'post':'create'})),
    path('homework/all/', HomeworkViewSet.as_view({'get':'list'})),
    path('homework/details/<int:pk>/', HomeworkViewSet.as_view({'get':'retrieve'})),
    path('homework/partialupdate/<int:pk>/', HomeworkViewSet.as_view({'patch': 'partial_update'})),
    path('homework/update/<int:pk>/', HomeworkViewSet.as_view({'put':'update'})),
    path('homework/delete/<int:pk>/', HomeworkViewSet.as_view({'delete':'destroy'})),
    
    path('notice/add/', NoticeViewSet.as_view({'post':'create'})),
    path('notice/all/', NoticeViewSet.as_view({'get':'list'})),
    path('notice/details/<int:pk>/', NoticeViewSet.as_view({'get':'retrieve'})),
    path('notice/partialupdate/<int:pk>/', NoticeViewSet.as_view({'patch': 'partial_update'})),
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