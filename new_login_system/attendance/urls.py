from django.urls import path
from .views import AttendanceViewset

urlpatterns = [
    path('add/', AttendanceViewset.as_view({'post':'create'})),
    path('all/', AttendanceViewset.as_view({'get':'list'})),
    path('details/<int:pk>/', AttendanceViewset.as_view({'get':'retrieve'})),
    path('partialupdate/<int:pk>/', AttendanceViewset.as_view({'patch': 'partial_update'})),
    path('update/<int:pk>/', AttendanceViewset.as_view({'put':'update'})),
    path('delete/<int:pk>/', AttendanceViewset.as_view({'delete':'destroy'})),
    path('by-date/', AttendanceViewset.as_view({'post':'by_date'})),
    path('summery/', AttendanceViewset.as_view({'post':'attendance_summary'})),
    path('by_student_id/', AttendanceViewset.as_view({'post':'by_student_id'})),
]