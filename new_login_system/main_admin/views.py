from django.shortcuts import render

from rest_framework import viewsets
from .models import Notices, Admins, Calender, Homework
from .serializers import NoticeSerializerserializer,Admins_serializer, CalenderSerializer, HomeworkSerializer
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

# jwt for each function
from rest_framework.permissions import IsAuthenticated
from .authentication import JWTAuthentication
from utils.base_viewsets import BaseCRUDViewSet
from .permissions import IsAdminOrReadOnly

class CalenderViewSet(BaseCRUDViewSet):
    queryset = Calender.objects.all()
    serializer_class = CalenderSerializer

class HomeworkViewSet(BaseCRUDViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    
class NoticeViewSet(BaseCRUDViewSet):
    queryset = Notices.objects.all().order_by('-created_at')
    serializer_class = NoticeSerializerserializer
      
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

