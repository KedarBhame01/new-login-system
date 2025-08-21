from rest_framework import serializers
from .models import Calender

class CalenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calender
        fields = '__all__'