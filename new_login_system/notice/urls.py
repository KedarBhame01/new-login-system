from django.urls import path
from .views import NoticeViewSet
urlpatterns = [
    path('notice/add/', NoticeViewSet.as_view({'post':'create'})),
    path('notice/all/', NoticeViewSet.as_view({'get':'list'})),
    path('notice/details/<int:pk>/', NoticeViewSet.as_view({'get':'retrieve'})),
    path('notice/partialupdate/<int:pk>/', NoticeViewSet.as_view({'patch': 'partial_update'})),
    path('notice/update/<int:pk>/', NoticeViewSet.as_view({'put':'update'})),
    path('notice/delete/<int:pk>/', NoticeViewSet.as_view({'delete':'destroy'})),
]