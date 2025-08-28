from rest_framework import serializers
from .models import FeeHistory

class FeeHistorySerializer(serializers.ModelSerializer):
    # img1_url = serializers.SerializerMethodField()
    class Meta:
        model = FeeHistory
        fields = '__all__'
        extra_kwargs = {
            'amount': {'default': 10000},
            'admin_remarks': {'read_only': True},
            'reviewed_date': {'read_only': True},
            'failure_reason': {'read_only': True}
        }

    def to_representation(self, instance):
        """Return full image URLs in API response"""
        representation = super().to_representation(instance)
        request = self.context.get('request')
        
        if instance.img1 and hasattr(instance.img1, 'url'):
            representation['img1'] = request.build_absolute_uri(instance.img1.url)
        else:
            representation['img1'] = None

        if instance.status == 'failed' and instance.failure_reason:
            failure_reasons = dict(instance._meta.get_field('failure_reason').choices)
            representation['failure_reason_display'] = failure_reasons.get(instance.failure_reason)
               
        return representation 

class fees_search_serializer(serializers.Serializer):   
    search_term = serializers.CharField(required=True)
    search_in = serializers.ChoiceField(
        choices=[" amount, payment_date, status, method, student_id_id, reviewed_date"]
    )