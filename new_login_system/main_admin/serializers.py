from rest_framework import serializers
from .models import Notices, Admins, Attendance, Calender

class Admins_serializer(serializers.ModelSerializer):
    class Meta:
        model = Admins
        fields = '__all__'

class NoticeSerializerserializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(required=True,allow_blank=True)
    class Meta:
        model = Notices
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ['id', 'student_name', 'created_at']

class DateOnlySerializer(serializers.Serializer):
    date = serializers.DateField()

class AttendanceSummaryInputSerializer(serializers.Serializer):
    student_id = serializers.IntegerField(required=True)

    class Meta:
            model = Attendance
            fields = 'student_id'

class CalenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calender
        fields = '__all__'