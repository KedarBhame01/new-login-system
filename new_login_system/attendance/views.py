from django.shortcuts import render

from .models import Attendance
from .serializers import AttendanceSerializer, AttendanceSummaryInputSerializer, DateOnlySerializer, Attendance_by_student_id_serializer
from rest_framework import status
from rest_framework.response import Response
from utils.base_viewsets import success_response, error_response

# from rest_framework.decorators import api_view

from rest_framework.decorators import action
from django.utils.dateparse import parse_date
# from drf_spectacular.utils import extend_schema

# for show swagger parameter
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

from utils.base_viewsets import BaseCRUDViewSet

# Create your views here.
class AttendanceViewset(BaseCRUDViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    @swagger_auto_schema(
        methods=['post'],
        request_body=Attendance_by_student_id_serializer,
        responses={200: AttendanceSerializer(many=True)}
    ) 
    @action(detail=False, methods=['post'], url_path='by_student_id')
    def by_student_id(self, request, *args, **kwargs):
            try:
                search_term = request.data.get('id')
                if not search_term:
                        return Response({"message": "Please provide a student_id"},
                                        status=status.HTTP_400_BAD_REQUEST)
                # search_in = request.data.get('search_in').lower()
                
                # Perform case-insensitive search by fieldname
                #    search_results = Students.objects.filter(
                #         Q(search_in=search_term))
                # search_results = Attendance.objects.none()
                
                search_results = self.queryset.filter(student_id=search_term)
               
                
                if not search_results.exists():
                    return error_response(
                    f"No attendance found matching this student_id '{search_term}'"
                    )
                serializer = AttendanceSerializer(search_results, many=True)

                return success_response("Search results", serializer.data)
            except Exception as e:
                return error_response(f"Error searching in attendance: {e}")   
    
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

    