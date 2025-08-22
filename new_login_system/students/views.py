from django.shortcuts import render
from .serializers import StudentSerializer, student_login_serializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Students
from main_admin.models import Admins
# for show swagger parameter
from drf_yasg.utils import swagger_auto_schema
# JWT authentication class
#for jwt json web token
import jwt
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

from utils.base_viewsets import BaseCRUDViewSet
from utils.base_viewsets import success_response, error_response
import logging

logger = logging.getLogger(__name__)
# Create your views here.
def login_page(request):
    return render(request, 'login.html')

def register_page(request):
    return render(request, 'register.html')

def dashboard_page(request):
    return render(request,'dashboard.html')
class StudentLoginAPI(ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = student_login_serializer
    
    @swagger_auto_schema(request_body=student_login_serializer)
    def login(self,request, *args, **kwargs):
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_type = serializer.validated_data.get('type')

            if user_type == 'student':
                email = serializer.validated_data.get('email')
                password = serializer.validated_data.get('password')
                try:
                    user = Students.objects.get(email=email)
                    if check_password(password, user.password):
                        return success_response("Student login successfully",
                                    serializer.data,
                                    code=status.HTTP_200_OK)
                    else:
                        return error_response('Invalid password', code=status.HTTP_400_BAD_REQUEST)
                except Students.DoesNotExist:
                    return error_response('Invalid email', code=status.HTTP_400_BAD_REQUEST)
                
            elif user_type == 'admin':
                # return Response({'message': 'cheack admin or not'},)
                email = serializer.validated_data.get('email')
                password = serializer.validated_data.get('password')
                try:
                    user = Admins.objects.get(email=email)
                    if check_password(password, user.password):
                        return success_response("Admin login successfully",
                                    serializer.data,
                                    code=status.HTTP_200_OK)
                    else:
                        return error_response('Invalid password', code=status.HTTP_400_BAD_REQUEST)
                except Admins.DoesNotExist:
                    return error_response('Invalid email', code=status.HTTP_400_BAD_REQUEST)

            else :
                return error_response('Invalid type select "admin" or "student"',code=status.HTTP_400_BAD_REQUEST)

        return error_response(serializer.errors, code=status.HTTP_400_BAD_REQUEST)
  
class student_API(BaseCRUDViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            if not data:
                return error_response('No data provided.', code=status.HTTP_400_BAD_REQUEST)

            # Check required fields
            for field in ['name', 'email', 'password']:
                if not data.get(field):
                    return error_response(f'Missing field: {field}', code=status.HTTP_400_BAD_REQUEST)

            # Check if email exists
            if Students.objects.filter(email=data['email']).exists():
                return error_response('Email already exists.', code=status.HTTP_409_CONFLICT)

            # Hash password
            data = data.copy()
            data['password'] = make_password(data['password'])

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return success_response(
                "Student registered successfully",
                                    serializer.data,
                                    code=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(f"Error creating student: {e}")
            return error_response('Registration failed. Please try again later.', code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
        