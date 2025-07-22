from django import forms
from .models import admin

class StudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = admin
        fields = '__all__'