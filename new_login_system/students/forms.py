from django import forms
from .models import Students

class StudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = Students
        fields = '__all__'