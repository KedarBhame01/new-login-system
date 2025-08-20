from rest_framework import serializers
from .models import Notices, Admins, Attendance, Calender, Homework

class Admins_serializer(serializers.ModelSerializer):
    class Meta:
        model = Admins
        fields = '__all__'
    def to_representation(self, instance):
        """Return full image URLs in API response"""
        representation = super().to_representation(instance)
        request = self.context.get('request')
        
        if instance.img1 and hasattr(instance.img1, 'url'):
            representation['img1'] = request.build_absolute_uri(instance.img1.url)
        else:
            representation['img1'] = None
            
        return representation 
    
class NoticeSerializerserializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(required=True,allow_blank=True)
    class Meta:
        model = Notices
        fields = '__all__'

class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = '__all__'
    def to_representation(self, instance):
        """Return full image URLs in API response"""
        representation = super().to_representation(instance)
        request = self.context.get('request')
        
        if instance.img1 and hasattr(instance.img1, 'url'):
            representation['img1'] = request.build_absolute_uri(instance.img1.url)
        else:
            representation['img1'] = None
            
        return representation 
        
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