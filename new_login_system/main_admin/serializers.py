from rest_framework import serializers
from .models import Notices

class notices_serializer(serializers.ModelSerializer):
    class Meta:
        model = Notices
        fields = '__all__'
