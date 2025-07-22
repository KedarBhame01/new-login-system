from rest_framework import serializers
from .models import admin

class admin_serializer(serializers.ModelSerializer):
    class Meta:
        model = admin
        fields = '__all__'