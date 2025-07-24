from django.shortcuts import render
from .serializers import student_serializer, student_login_serializer
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
from drf_yasg import openapi
#for jwt json web token
import jwt
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

# Create your views here.
def login_page(request):
    return render(request, 'login.html')

def register_page(request):
    return render(request, 'register.html')

def dashboard_page(request):
    return render(request,'dashboard.html')

class StudentLoginAPI(APIView):
    queryset = Students.objects.all()
    serializer_class = student_login_serializer
    
    @swagger_auto_schema(request_body=student_login_serializer)
    def post(self,request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            ptype = serializer.validated_data.get('type')
            if ptype == 'student':
                email = serializer.validated_data.get('email')
                password = serializer.validated_data.get('password')

                try:
                    admin_user = Students.objects.get(email=email)
                    
                    if check_password(password, admin_user.password):
                        # return Response({'success': True,
                        #     'message': 'valid User'}, status=status.HTTP_200_OK)
                        return self.generate_token_response(admin_user)
                    else:
                        return Response({'message': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
            
                except Students.DoesNotExist:
                    return Response({'message': 'Invalid email'}, status=status.HTTP_401_UNAUTHORIZED)
            elif ptype == 'admin':
                # return Response({'message': 'cheack admin or not'},)
                email = serializer.validated_data.get('email')
                password = serializer.validated_data.get('password')

                try:
                    admin_user = Admins.objects.get(email=email)
                    
                    if check_password(password, admin_user.password):
                        # return Response({'success': True,
                        #     'message': 'valid User'}, status=status.HTTP_200_OK)
                        return self.generate_token_response(admin_user)
                    else:
                        return Response({'message': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
            
                except Admins.DoesNotExist:
                    return Response({'message': 'Invalid email'}, status=status.HTTP_401_UNAUTHORIZED)
            else :
                return Response({'message': 'Invalid type select "admin" or "student"'},)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_token_response(self, admin_user):
        now = timezone.now()
        payload = {
            'uid' : admin_user.id,
            'email': admin_user.email,
            'exp' : now +timedelta(days=1),
            'iat' : now,
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return Response({
            'success': True,
            'message': 'Login successful',
            'id': admin_user.id,
            'email': admin_user.email,
            'token': token,
        },status=status.HTTP_200_OK, headers={'Authorization':f'bearer{token}'})

class student_API(ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = student_serializer

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
        
# @api_view(['POST'])
# def register_function(request):
#     if request.method == 'POST':
#         data = request.data.copy()
#         # Hashing the password before saving
#         if 'password' in data:
#             data['password'] = make_password(data['password'])

#         serializer = student_serializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'success': True, 'data': serializer.data}, status=201)
#         return Response(serializer.errors, status=400)
#     else:
#         return Response({'error': 'Only POST method is allowed.'}, status=405)

# @api_view(['POST'])
# def login_function(request):
#     serializer = student_login_serializer
#     if serializer.is_valid():
#         aemail = serializer.validated_data.get('aemail')
#         apassword = serializer.validated_data.get('apassword')

#         # email = request.data.get('email')
#         # password = request.data.get('password')
        
#         # if not email or not password:
#         #     return Response({'success': False, 'message': 'Email and password are required.'}, status=400)
    
#         try:
#             admin_user = Students.objects.get(aemail=aemail)
            
#             if admin_user.password == apassword:
#                 return Response({
#                     'message': 'valid User'}, status=status.HTTP_200_ok)
#             else:
#                 return Response({'message': 'Invalid password'}, status=status.HTTP_401_AUTHORIZED)
    
#         except admin.DoesNotExist:
#             return Response({'message': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#     return Response(serializer.errors, status=status.HTTP_401_BAD_REQUEST)

