from django.shortcuts import render

from rest_framework import viewsets
from .models import Admins
from .serializers import Admins_serializer
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
# from rest_framework.decorators import api_view

from rest_framework.decorators import action
from django.utils.dateparse import parse_date
# from drf_spectacular.utils import extend_schema

# for show swagger parameter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

from utils.base_viewsets import BaseCRUDViewSet
from utils.base_viewsets import success_response, error_response
      
class AdminViewSet(BaseCRUDViewSet):
    queryset = Admins.objects.all()
    serializer_class = Admins_serializer

    def create(self, request, *args, **kwargs):
        try:
            mutable_data = request.data.copy()
            if 'password' in mutable_data:
                mutable_data['password'] = make_password(mutable_data['password'])
            serializer = self.get_serializer(data = mutable_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return success_response("Record created successfully",
                                    serializer.data,
                                    code=status.HTTP_201_CREATED)
        except Exception as e:
            return error_response(f"Error creating record: {e}")
    
