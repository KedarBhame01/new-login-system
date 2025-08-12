from django.shortcuts import render

from rest_framework import viewsets
from .models import Notices, Admins, Attendance, Calender, Homework
from .serializers import NoticeSerializerserializer,Admins_serializer, AttendanceSerializer, DateOnlySerializer, AttendanceSummaryInputSerializer, CalenderSerializer, HomeworkSerializer
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

from .permissions import IsAdminOrReadOnly

class CalenderViewSet(viewsets.ModelViewSet):
    queryset = Calender.objects.all()
    serializer_class = CalenderSerializer

class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    
class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notices.objects.all().order_by('-created_at')
    serializer_class = NoticeSerializerserializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAdminOrReadOnly]
    # permission_classes = [IsAuthenticated]
    def list(self, request, *args, **kwargs):
        try:
            admin = Notices.objects.all()
            serializer = self.get_serializer(admin, many=True)
            api_response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message':'All notice',
                'all_notice': serializer.data
            }
            return Response(api_response)
        except Exception as e:
            error_msg = 'An error occurred while fetching records:{}'.format(str(e))
            error_response ={
                'status': 'error',
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': error_msg,
            }
            return Response(error_response)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            api_response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message':'notice',
                'notice': serializer.data
            }
            return Response(api_response)
        except Exception as e:
            error_msg = 'An error occurred while fetching records:{}'.format(str(e))
            error_response ={
                'status': 'error',
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': error_msg,
            }
            return Response(error_response)

    def create(self, request, *args, **kwargs):
                    try:
                              serializer = self.get_serializer(data=request.data)
                              serializer.is_valid(raise_exception=True)
                              serializer.save()
                              api_response = {
                                        'status': 'success',
                                        'code': status.HTTP_200_OK,
                                        'message': 'notice added successfully',
                                        'notice': serializer.data,
                              }
                              return Response(api_response)
                    except Exception as e:
                              error_msg = 'An error occurred: {}'.format(str(e))
                              error_response = {
                                        'status': 'error',
                                        'code': status.HTTP_400_BAD_REQUEST,
                                        'message': error_msg,
                              }
                              return Response(error_response)

    def update(self, request, *args, **kwargs):
            try:
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                api_response = {
                      'status': 'success',
                      'code': status.HTTP_200_OK,
                      'message': 'notice updated successfully',
                      'updated_notice': serializer.data,
                }
                return Response(api_response)
            except Exception as e:
                error_msg = 'An error occurred: {}'.format(str(e))
                error_response = {
                      'status': 'error',
                      'code': status.HTTP_400_BAD_REQUEST,
                      'message': error_msg,
                }
                return Response(error_response)

    def destroy(self, request, *args, **kwargs):
            try:
                instance = self.get_object()
                instance.delete()
                api_response = {
                      'status': 'success',
                      'code': status.HTTP_200_OK,
                      'message': 'notice deleted successfully',
                }
                return Response(api_response)
            except Exception as e:
                error_msg = 'An error occurred: {}'.format(str(e))
                error_response = {
                      'status': 'error',
                      'code': status.HTTP_400_BAD_REQUEST,
                      'message': error_msg,
                }
                return Response(error_response)



class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admins.objects.all()
    serializer_class = Admins_serializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

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

class AttendanceViewset(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    # @extend_schema(
    #     request=AttendanceSummaryInputSerializer,

    # )
    @swagger_auto_schema(
        methods=['post'],
        request_body= AttendanceSummaryInputSerializer,
        responses={200: AttendanceSerializer(many=True)}
    )
    @action(detail=False, methods=['post'], url_path='summary')
    def attendance_summary(self, request):
        serializer = AttendanceSummaryInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student_id = serializer.validated_data['student_id']

        if not student_id:
            return Response({
                'success': False,
                'message': 'Please provide student_id in the request body.'
            }, status=400)

        attendance_qs = self.queryset.filter(student_id=student_id)
        total_days = attendance_qs.count()
        present_days = attendance_qs.filter(present=True).count()

        return Response({
            'success': True,
            'student_id': student_id,
            'present_days': present_days,
            'total_days': total_days,
            'message': f"Student {student_id} was present {present_days} out of {total_days} days "
        })

    @swagger_auto_schema(
        methods=['post'],
        request_body=DateOnlySerializer,
        responses={200: AttendanceSerializer(many=True)}
    )
    @action(detail=False, methods=['post'], url_path='by-date')
    def by_date(self, request):
        # now request.data only needs {"date": "YYYY-MM-DD"}
        date_str = request.data.get('date')
        if not date_str:
            return Response({'error': 'date field missing'}, status=400)
        date_obj = parse_date(date_str)
        if not date_obj:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400
            )
        records = self.queryset.filter(date=date_obj)
        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data, status=200)

    def list(self, request, *args, **kwargs):
        try:
            admin = Attendance.objects.all()
            serializer = self.get_serializer(admin, many=True)
            api_response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message':'All attendance',
                'all_attendance': serializer.data
            }
            return Response(api_response)
        except Exception as e:
            error_msg = 'An error occurred while fetching records:{}'.format(str(e))
            error_response ={
                'status': 'error',
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': error_msg,
            }
            return Response(error_response)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            api_response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message':'attendance',
                'attendance': serializer.data
            }
            return Response(api_response)
        except Exception as e:
            error_msg = 'An error occurred while fetching records:{}'.format(str(e))
            error_response ={
                'status': 'error',
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': error_msg,
            }
            return Response(error_response)

    def create(self, request, *args, **kwargs):
                    try:
                              serializer = self.get_serializer(data=request.data)
                              serializer.is_valid(raise_exception=True)
                              serializer.save()
                              api_response = {
                                        'status': 'success',
                                        'code': status.HTTP_200_OK,
                                        'message': 'Attendance added successfully',
                                        'attendance': serializer.data,
                              }
                              return Response(api_response)
                    except Exception as e:
                              error_msg = 'An error occurred: {}'.format(str(e))
                              error_response = {
                                        'status': 'error',
                                        'code': status.HTTP_400_BAD_REQUEST,
                                        'message': error_msg,
                              }
                              return Response(error_response)

    def update(self, request, *args, **kwargs):
            try:
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                api_response = {
                      'status': 'success',
                      'code': status.HTTP_200_OK,
                      'message': 'Attendance updated successfully',
                      'updated_attendance': serializer.data,
                }
                return Response(api_response)
            except Exception as e:
                error_msg = 'An error occurred: {}'.format(str(e))
                error_response = {
                      'status': 'error',
                      'code': status.HTTP_400_BAD_REQUEST,
                      'message': error_msg,
                }
                return Response(error_response)

    def destroy(self, request, *args, **kwargs):
            try:
                instance = self.get_object()
                instance.delete()
                api_response = {
                      'status': 'success',
                      'code': status.HTTP_200_OK,
                      'message': 'Attendance deleted successfully',
                }
                return Response(api_response)
            except Exception as e:
                error_msg = 'An error occurred: {}'.format(str(e))
                error_response = {
                      'status': 'error',
                      'code': status.HTTP_400_BAD_REQUEST,
                      'message': error_msg,
                }
                return Response(error_response)
