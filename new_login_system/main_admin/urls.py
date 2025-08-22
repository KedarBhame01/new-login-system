from django.contrib import admin
from django.urls import path
from .views import AdminViewSet
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/add/',AdminViewSet.as_view({'post':'create'})),
    path('admin/all/', AdminViewSet.as_view({'get':'list'})),
    path('admin/details/<int:pk>/', AdminViewSet.as_view({'get':'retrieve'})),
    # path('admin/partialupdate/<int:pk>/', AdminViewSet.as_view({'patch': 'partial_update'})),
    # path('admin/update/<int:pk>/', AdminViewSet.as_view({'put':'update'})),
    path('admin/delete/<int:pk>/', AdminViewSet.as_view({'delete':'destroy'})), 

    # Web pages
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('students/', views.admin_students, name='admin_students'),
    path('fees/', views.admin_fees, name='admin_fees'),
    path('attendance/', views.admin_attendance, name='admin_attendance'),
    path('calendar/', views.admin_calendar, name='admin_calendar'),
    path('homework/', views.admin_homework, name='admin_homework'),
    path('notice/', views.admin_notices, name='admin_notices'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)