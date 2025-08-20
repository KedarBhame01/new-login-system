from django.shortcuts import render
from .serializers import StudentSerializer, student_login_serializer, FeeHistorySerializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Students, FeeHistory
from main_admin.models import Admins
# for show swagger parameter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# JWT authentication class

def success_response(message, data=None, code=status.HTTP_200_OK, extra=None):
    response = {
        "status": "success",
        "code": code,
        "message": message,
    }
    if data is not None:
        response["data"] = data
    if extra:
        response.update(extra)
    return Response(response, status=code)


def error_response(message, code=status.HTTP_400_BAD_REQUEST):
    response = {
        "status": "error",
        "code": code,
        "message": message,
    }
    return Response(response, status=code)

import os
#for jwt json web token
import jwt
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

from utils.base_viewsets import BaseCRUDViewSet
# Create your views here.
def login_page(request):
    return render(request, 'login.html')

def register_page(request):
    return render(request, 'register.html')

def dashboard_page(request):
    return render(request,'dashboard.html')

@api_view(['POST'])
def verify_token(request):
    token = request.data.get('token')
    if not token:
        return Response({'valid': False, 'message': 'Token not provided'}, status=400)
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get('id')
        user_type = payload.get('user_type')
        if user_type == 'admin':
            user = Admins.objects.get(id=user_id)

        elif user_type == 'student':
            user = Students.objects.get(id=user_id)

        else:
                return Response({'valid': False, 'message': 'User does not exist'}, status=401)
        return Response({'valid': True, 'user_type': user_type, 'user_id': user_id})

    except jwt.ExpiredSignatureError:
        return Response({'valid': False, 'message': 'Token expired'})
    except jwt.InvalidTokenError:
        return Response({'valid': False, 'message': 'Invalid token'})
class StudentLoginAPI(APIView):
    queryset = Students.objects.all()
    serializer_class = student_login_serializer
    
    @swagger_auto_schema(request_body=student_login_serializer)
    def post(self,request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user_type = serializer.validated_data.get('type')
            if user_type == 'student':
                email = serializer.validated_data.get('email')
                password = serializer.validated_data.get('password')

                try:
                    user = Students.objects.get(email=email)
                    
                    if check_password(password, user.password):
                        # return Response({'success': True,
                        #     'message': 'valid User'}, status=status.HTTP_200_OK)
                        return self.generate_token_response(user, user_type)
                    else:
                        return Response({'message': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
            
                except Students.DoesNotExist:
                    return Response({'message': 'Invalid email'}, status=status.HTTP_401_UNAUTHORIZED)
            elif user_type == 'admin':
                # return Response({'message': 'cheack admin or not'},)
                email = serializer.validated_data.get('email')
                password = serializer.validated_data.get('password')

                try:
                    user = Admins.objects.get(email=email)
                    
                    if check_password(password, user.password):
                        # return Response({'success': True,
                        #     'message': 'valid User'}, status=status.HTTP_200_OK)
                        return self.generate_token_response(user, user_type)
                    else:
                        return Response({'message': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
            
                except Admins.DoesNotExist:
                    return Response({'message': 'Invalid email'}, status=status.HTTP_401_UNAUTHORIZED)
            else :
                return Response({'message': 'Invalid type select "admin" or "student"'},)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_token_response(self, user, user_type):
        now = timezone.now()
        payload = {
            'user_type': user_type,
            'id' : user.id,
            'email': user.email,
            'exp' : int((now +timedelta(days=1)).timestamp()),
            'iat' : int(now.timestamp()),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return Response({
            'success': True,
            'message': 'Login successful',
            'user_type': user_type,
            'id': user.id,
            'email': user.email,
            # 'token': token,
        },status=status.HTTP_200_OK, headers={'Authorization':f'Bearer {token}'})

class student_API(BaseCRUDViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer

class FeeHistoryAPI(BaseCRUDViewSet):
    queryset = FeeHistory.objects.all()
    serializer_class = FeeHistorySerializer

    def get_queryset(self):
        student_id = self.request.query_params.get('student_id')
        if student_id:
            return FeeHistory.objects.filter(student_id=student_id)
        return super().get_queryset()

    @action(detail=False, methods=['post'], url_path='pay-fees')
    def pay_fees(self, request):
        try:
            student_id = request.data.get('student_id')
            try:
                amount = int(request.data.get('amount', 0))
            except (TypeError, ValueError):
                return error_response("Invalid amount.", code=status.HTTP_400_BAD_REQUEST)

            remarks = request.data.get('remarks', '')
            try:
                student = Students.objects.get(id=student_id)
            except Students.DoesNotExist:
                return error_response("Student not found.", code=status.HTTP_404_NOT_FOUND)

            # Strict amount check - amount must equal pending_fees
            if amount != student.pending_fees:
                return error_response(
                    f"Payment must be exactly the pending fees: {student.pending_fees}",
                    code=status.HTTP_400_BAD_REQUEST
                )

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return success_response(
                "Fee payment recorded",
                serializer.data,
                code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return error_response(f"Error creating record: {e}")        