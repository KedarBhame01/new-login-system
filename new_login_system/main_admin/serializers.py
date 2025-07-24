from rest_framework import serializers
from .models import admin

class admin_serializer(serializers.ModelSerializer):
    class Meta:
        model = admin
        fields = '__all__'

class admin_login_serializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)