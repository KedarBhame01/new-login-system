from rest_framework import serializers
from .models import Notices

class NoticeSerializerserializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(required=True,allow_blank=True)
    class Meta:
        model = Notices
        fields = '__all__'
