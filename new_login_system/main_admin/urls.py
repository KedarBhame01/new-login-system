from django.contrib import admin
from django.urls import path
from .views import AdminViewSet
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
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