from django.shortcuts import render

from rest_framework import viewsets
from .models import Notices,Admins
from .serializers import notices_serializer,Admins_serializer
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

# def verify_token(request):
#     data = request.json
#     token = data.get('token')
#     if valid_token(token):
#         return Response[{'valid': True}]
#     else:
#         return Response[{'valid': False}]
class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notices.objects.all().order_by('-created_at')
    serializer_class = notices_serializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    
class Admin_API(viewsets.ModelViewSet):
    queryset = Admins.objects.all()
    serializer_class = Admins_serializer
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=Admins_serializer)
    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            if 'password'in data:
                data['password'] = make_password(data['password'])

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response={'success': True, 
                          'data': serializer.data, 
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