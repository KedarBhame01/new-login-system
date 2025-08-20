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
    # img1_url = serializers.SerializerMethodField()
    class Meta:
        model = FeeHistory
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
    