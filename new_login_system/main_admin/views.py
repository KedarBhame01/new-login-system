from django.shortcuts import render
from .serializers import admin_serializer
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
def login_page(request):
    return render(request, 'login.html')

def register_page(request):
    return render(request, 'register.html')

@api_view(['POST'])
def register_function(request):
    if request.method == 'POST':
        data = request.data.copy()
        # Hashing the password before saving
        if 'password' in data:
            data['password'] = make_password(data['password'])

        serializer = admin_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data}, status=201)
        return Response(serializer.errors, status=400)
    else:
        return Response({'error': 'Only POST method is allowed.'}, status=405)