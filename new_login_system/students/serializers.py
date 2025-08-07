from rest_framework import serializers
from .models import Students, FeeHistory

class StudentSerializer(serializers.ModelSerializer):
    pending_fees = serializers.ReadOnlyField()
    class Meta:
        model = Students
        fields = '__all__'

class student_login_serializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    # type = serializers.CharField(choices=[('admin','admin'),('student','student')],required=True)
    type = serializers.ChoiceField(choices=['admin', 'student'])

class FeeHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeHistory
        fields = '__all__'
