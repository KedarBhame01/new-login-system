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
      
class AdminViewSet(BaseCRUDViewSet):
    queryset = Admins.objects.all()
    serializer_class = Admins_serializer

    @swagger_auto_schema(request_body=Admins_serializer)
    def create(self, request, *args, **kwargs):
        try:
            request_data = request.data.copy()
            if 'password'in request_data:
                request_data['password'] = make_password(request_data['password'])

            serializer = self.get_serializer(data=request_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response={'success': True, 
                          'data': request_data, 
                          'code': status.HTTP_201_CREATED,
                          }
            return Response(api_response)
        except Exception as e:
            error_msg = 'An error occurred: {}'.format(str(e))
            error_response ={ 'success': False,
                             'code': status.HTTP_400_BAD_REQUEST,
                             'message': error_msg,
                             }
            return Response(error_response)

