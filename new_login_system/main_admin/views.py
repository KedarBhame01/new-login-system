from django.shortcuts import render
from .serializers import admin_serializer, admin_login_serializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import admin

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
def login_page(request):
    return render(request, 'login.html')

def register_page(request):
    return render(request, 'register.html')

def dashboard_page(request):
    return render(request,'dashboard.html')

class AdminLoginAPI(APIView):
    queryset = admin.objects.all()
    serializer_class = admin_login_serializer
    
    @swagger_auto_schema(request_body=admin_login_serializer)
    def post(self,request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            try:
                admin_user = admin.objects.get(email=email)
                
                if check_password(password, admin_user.password):
                    return Response({'success': True,
                        'message': 'valid User'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
        
            except admin.DoesNotExist:
                return Response({'message': 'Invalid email'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Admin_API(ModelViewSet):
    queryset = admin.objects.all()
    serializer_class = admin_serializer

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

#         serializer = admin_serializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'success': True, 'data': serializer.data}, status=201)
#         return Response(serializer.errors, status=400)
#     else:
#         return Response({'error': 'Only POST method is allowed.'}, status=405)

# @api_view(['POST'])
# def login_function(request):
#     serializer = admin_login_serializer
#     if serializer.is_valid():
#         aemail = serializer.validated_data.get('aemail')
#         apassword = serializer.validated_data.get('apassword')

#         # email = request.data.get('email')
#         # password = request.data.get('password')
        
#         # if not email or not password:
#         #     return Response({'success': False, 'message': 'Email and password are required.'}, status=400)
    
#         try:
#             admin_user = admin.objects.get(aemail=aemail)
            
#             if admin_user.password == apassword:
#                 return Response({
#                     'message': 'valid User'}, status=status.HTTP_200_ok)
#             else:
#                 return Response({'message': 'Invalid password'}, status=status.HTTP_401_AUTHORIZED)
    
#         except admin.DoesNotExist:
#             return Response({'message': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#     return Response(serializer.errors, status=status.HTTP_401_BAD_REQUEST)