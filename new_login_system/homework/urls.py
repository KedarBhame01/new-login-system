from django.urls import path
from .views import HomeworkViewSet

urlpatterns = [
    path('add/', HomeworkViewSet.as_view({'post':'create'})),
    path('all/', HomeworkViewSet.as_view({'get':'list'})),
    path('details/<int:pk>/', HomeworkViewSet.as_view({'get':'retrieve'})),
    path('partialupdate/<int:pk>/', HomeworkViewSet.as_view({'patch': 'partial_update'})),
    path('update/<int:pk>/', HomeworkViewSet.as_view({'put':'update'})),
    path('delete/<int:pk>/', HomeworkViewSet.as_view({'delete':'destroy'})),
]