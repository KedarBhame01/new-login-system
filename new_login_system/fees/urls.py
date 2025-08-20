from django.contrib import admin
from django.urls import path
from .views import FeeHistoryAPI

urlpatterns = [
    path('pay/', FeeHistoryAPI.as_view({'post':'pay_fees'})),
    # path('add/', FeeHistoryAPI.as_view({'post':'create'})),
    path('all/', FeeHistoryAPI.as_view({'get':'list'})),
    path('details/<int:pk>/', FeeHistoryAPI.as_view({'get':'retrieve'})),
    path('partialupdate/<int:pk>/', FeeHistoryAPI.as_view({'patch': 'partial_update'})),
    path('update/<int:pk>/', FeeHistoryAPI.as_view({'put':'update'})),
    path('delete/<int:pk>/', FeeHistoryAPI.as_view({'delete':'destroy'})),
    
]

