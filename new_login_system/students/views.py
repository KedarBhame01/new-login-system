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
# class StudentLoginAPI(ModelViewSet):
#     queryset = Students.objects.all()
#     serializer_class = student_login_serializer
    
#     @swagger_auto_schema(request_body=student_login_serializer)
#     def login(self,request, *args, **kwargs):
        
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             user_type = serializer.validated_data.get('type')

#             if user_type == 'student':
#                 email = serializer.validated_data.get('email')
#                 password = serializer.validated_data.get('password')
#                 try:
#                     user = Students.objects.get(email=email)
#                     if check_password(password, user.password):
#                         return success_response("Student login successfully",
#                                     serializer.data,
#                                     code=status.HTTP_200_OK)
#                     else:
#                         return error_response('Invalid password', code=status.HTTP_400_BAD_REQUEST)
#                 except Students.DoesNotExist:
#                     return error_response('Invalid email', code=status.HTTP_400_BAD_REQUEST)
                
#             elif user_type == 'admin':
#                 # return Response({'message': 'cheack admin or not'},)
#                 email = serializer.validated_data.get('email')
#                 password = serializer.validated_data.get('password')
#                 try:
#                     user = Admins.objects.get(email=email)
#                     if check_password(password, user.password):
#                         return success_response("Admin login successfully",
#                                     serializer.data,
#                                     code=status.HTTP_200_OK)
#                     else:
#                         return error_response('Invalid password', code=status.HTTP_400_BAD_REQUEST)
#                 except Admins.DoesNotExist:
#                     return error_response('Invalid email', code=status.HTTP_400_BAD_REQUEST)

#             else :
#                 return error_response('Invalid type select "admin" or "student"',code=status.HTTP_400_BAD_REQUEST)

#         return error_response(serializer.errors, code=status.HTTP_400_BAD_REQUEST)
  
# Add these new view functions to your students/views.py (keep existing code)

def profile_page(request):
    """Student profile page"""
    try:
        return render(request, 'student-profile.html')
    except Exception as e:
        logger.error(f"Error loading profile page: {e}")
        return render(request, 'error.html', {'message': 'Unable to load profile page'})

def fees_page(request):
    """Student fees page"""
    try:
        return render(request, 'student-fees.html')
    except Exception as e:
        logger.error(f"Error loading fees page: {e}")
        return render(request, 'error.html', {'message': 'Unable to load fees page'})

def attendance_page(request):
    """Student attendance page"""
    try:
        return render(request, 'student-attendance.html')
    except Exception as e:
        logger.error(f"Error loading attendance page: {e}")
        return render(request, 'error.html', {'message': 'Unable to load attendance page'})

def homework_page(request):
    """Student homework page"""
    try:
        return render(request, 'student-homework.html')
    except Exception as e:
        logger.error(f"Error loading homework page: {e}")
        return render(request, 'error.html', {'message': 'Unable to load homework page'})

def notices_page(request):
    """Student notices page"""
    try:
        return render(request, 'student-notices.html')
    except Exception as e:
        logger.error(f"Error loading notices page: {e}")
        return render(request, 'error.html', {'message': 'Unable to load notices page'})
def attendance_page(request):
    """Student attendance view page"""
    try:
        return render(request, 'student-attendance.html')
    except Exception as e:
        logger.error(f"Error loading attendance page: {e}")
        return render(request, 'error.html', {'message': 'Unable to load attendance page'})

def homework_page(request):
    """Student homework view page"""
    try:
        return render(request, 'student-homework.html')
    except Exception as e:
        logger.error(f"Error loading homework page: {e}")
        return render(request, 'error.html', {'message': 'Unable to load homework page'})

def notices_page(request):
    """Student notices view page"""
    try:
        return render(request, 'student-notices.html')
    except Exception as e:
        logger.error(f"Error loading notices page: {e}")
        return render(request, 'error.html', {'message': 'Unable to load notices page'})
    
class StudentLoginAPI(ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = student_login_serializer
    
    @swagger_auto_schema(request_body=student_login_serializer)
    def login(self, request, *args, **kwargs):
        """Login API with comprehensive error handling"""
        try:
            # 🔹 Check if request data exists
            if not request.data:
                return error_response(
                    'No data provided. Please send email, password and type.', 
                    code=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = self.serializer_class(data=request.data)

            if not serializer.is_valid():
                # 🔹 Better error messages for validation
                error_messages = []
                for field, errors in serializer.errors.items():
                    error_messages.append(f"{field}: {', '.join(errors)}")
                return error_response(
                    f"Validation failed: {'; '.join(error_messages)}", 
                    code=status.HTTP_400_BAD_REQUEST
                )

            user_type = serializer.validated_data.get('type')
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            
            # 🔹 Validate required fields
            if not email:
                return error_response('Email is required', code=status.HTTP_400_BAD_REQUEST)
            if not password:
                return error_response('Password is required', code=status.HTTP_400_BAD_REQUEST)
            if not user_type:
                return error_response('User type is required', code=status.HTTP_400_BAD_REQUEST)

            if user_type == 'student':
                try:
                    user = Students.objects.get(email=email)
                    data ={
                        "user_type": user_type,
                        "id": user.id,
                        'name': user.name,
                        'email': user.email,
                        'j_date': user.j_date,
                        'phone_no': user.phone_no,
                        'total_fees': user.total_fees,
                        'paid_fees': user.paid_fees,
                        'pending_fees': user.pending_fees,

                    }
                    # 🔹 Add password check with better error handling
                    try:
                        if check_password(password, user.password):
                            logger.info(f"Student login successful for: {email}")
                            return success_response(
                                "Student login successful",
                                data,
                                code=status.HTTP_200_OK
                            )
                        else:
                            logger.warning(f"Invalid password attempt for student: {email}")
                            return error_response(
                                'Invalid password. Please check your password and try again.', 
                                code=status.HTTP_401_UNAUTHORIZED
                            )
                    except Exception as pwd_error:
                        logger.error(f"Password check error for student {email}: {pwd_error}")
                        return error_response(
                            'Authentication failed. Please try again.', 
                            code=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
                
                except Students.DoesNotExist:
                    logger.warning(f"Login attempt with non-existent student email: {email}")
                    return error_response(
                        'No student account found with this email. Please check your email or register.', 
                        code=status.HTTP_404_NOT_FOUND
                    )
                except Exception as e:
                    logger.error(f"Unexpected error during student login: {e}")
                    return error_response(
                        'Login failed due to server error. Please try again later.', 
                        code=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            elif user_type == 'admin':
                try:
                    user = Admins.objects.get(email=email)
                    
                    # 🔹 Add password check with better error handling
                    try:
                        if check_password(password, user.password):
                            logger.info(f"Admin login successful for: {email}")
                            return success_response(
                                "Admin login successful",
                                serializer.data,
                                code=status.HTTP_200_OK
                            )
                        else:
                            logger.warning(f"Invalid password attempt for admin: {email}")
                            return error_response(
                                'Invalid password. Please check your password and try again.', 
                                code=status.HTTP_401_UNAUTHORIZED
                            )
                    except Exception as pwd_error:
                        logger.error(f"Password check error for admin {email}: {pwd_error}")
                        return error_response(
                            'Authentication failed. Please try again.', 
                            code=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
                
                except Admins.DoesNotExist:
                    logger.warning(f"Login attempt with non-existent admin email: {email}")
                    return error_response(
                        'No admin account found with this email. Please contact system administrator.', 
                        code=status.HTTP_404_NOT_FOUND
                    )
                except Exception as e:
                    logger.error(f"Unexpected error during admin login: {e}")
                    return error_response(
                        'Login failed due to server error. Please try again later.', 
                        code=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            else:
                return error_response(
                    'Invalid user type. Please select either "admin" or "student".', 
                    code=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            logger.error(f"Unexpected error in login API: {e}")
            return error_response(
                'An unexpected error occurred. Please try again later.', 
                code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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

        
        