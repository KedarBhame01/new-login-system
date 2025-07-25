from django.shortcuts import render

from rest_framework import viewsets
from .models import Notices
from .serializers import notices_serializer
# Create your views here.

class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notices.objects.all().order_by('-created_at')
    serializer_class = notices_serializer