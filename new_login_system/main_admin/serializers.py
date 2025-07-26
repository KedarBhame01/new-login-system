from rest_framework import serializers
from .models import Notices,Admins


class NoticeSerializerserializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(required=True,allow_blank=True)
    class Meta:
        model = Notices
        fields = '__all__'
class Admins_serializer(serializers.ModelSerializer):
    class Meta:
        model = Admins
        fields = '__all__'