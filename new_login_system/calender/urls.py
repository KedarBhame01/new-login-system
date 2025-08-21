from django.urls import path
from .views import CalenderViewSet

urlpatterns = [
    
    path('add/', CalenderViewSet.as_view({'post':'create'})),
    path('all/', CalenderViewSet.as_view({'get':'list'})),
    path('details/<int:pk>/', CalenderViewSet.as_view({'get':'retrieve'})),
    path('partialupdate/<int:pk>/', CalenderViewSet.as_view({'patch': 'partial_update'})),
    path('update/<int:pk>/', CalenderViewSet.as_view({'put':'update'})),
    path('delete/<int:pk>/', CalenderViewSet.as_view({'delete':'destroy'})),
]