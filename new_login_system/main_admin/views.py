from django.shortcuts import render

from rest_framework import viewsets
from .models import Notices,Admins
from .serializers import NoticeSerializerserializer,Admins_serializer
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response

# for show swagger parameter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

# jwt for each function
from rest_framework.permissions import IsAuthenticated
from .authentication import JWTAuthentication

from .permissions import IsAdminOrReadOnly

class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notices.objects.all().order_by('-created_at')
    serializer_class = NoticeSerializerserializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    
class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admins.objects.all()
    serializer_class = Admins_serializer
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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
                          'data': serializer.request_data, 
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