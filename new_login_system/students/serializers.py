from rest_framework import serializers
from .models import Students

class StudentSerializer(serializers.ModelSerializer):
    pending_fees = serializers.ReadOnlyField()
    paid_fees = serializers.ReadOnlyField()
    class Meta:
        model = Students
        fields = '__all__'
        extra_kwargs = {
            'total_fees': {'default': 10000},
            'phone_no' : {'default': 1234567890}
        }

class student_login_serializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    # type = serializers.CharField(choices=[('admin','admin'),('student','student')],required=True)
    type = serializers.ChoiceField(choices=['admin', 'student'])
    
class student_search_serializer(serializers.Serializer):   
    search_term = serializers.CharField(required=True)
    search_in = serializers.ChoiceField(
        choices=['name', 'email', 'phone_no', 'account','total_fees','j_date']
        # default='all'
    )