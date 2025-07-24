from rest_framework import serializers
from .models import Students

class student_serializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = '__all__'

class student_login_serializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    type = serializers.CharField(required=True)