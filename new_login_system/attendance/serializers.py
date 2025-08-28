from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ['id', 'student_name', 'created_at']

class AttendanceSummaryInputSerializer(serializers.Serializer):
    student_id = serializers.IntegerField(required=True)

    class Meta:
            model = Attendance
            fields = 'student_id'

class DateOnlySerializer(serializers.Serializer):
    date = serializers.DateField(required=True)

class Attendance_by_student_id_serializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)