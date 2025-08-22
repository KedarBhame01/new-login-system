from rest_framework import serializers
from .models import FeeHistory

class FeeHistorySerializer(serializers.ModelSerializer):
    # img1_url = serializers.SerializerMethodField()
    class Meta:
        model = FeeHistory
        fields = '__all__'
        extra_kwargs = {
            'amount': {'default': 10000}
        }

    def to_representation(self, instance):
        """Return full image URLs in API response"""
        representation = super().to_representation(instance)
        request = self.context.get('request')
        
        if instance.img1 and hasattr(instance.img1, 'url'):
            representation['img1'] = request.build_absolute_uri(instance.img1.url)
        else:
            representation['img1'] = None
            
        return representation 