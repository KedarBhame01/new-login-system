from django.shortcuts import render
from .serializers import admin_serializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import admin

# Create your views here.
def login_page(request):
    return render(request, 'login.html')

def register_page(request):
    return render(request, 'register.html')

def dashboard_page(request):
    return render(request,'dashboard.html')

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

@api_view(['POST'])
def login_function(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({'success': False, 'message': 'Email and password required'}, status=400)
        try:
            tadmin = admin.objects.get(email=email)
            if check_password(password, tadmin.password):
                return Response({'success': True,
                                'message': 'Login successful',
                                'student':
                                    {'id': tadmin.id,
                                    'name':tadmin.name,
                                    'email': tadmin.email
                                    }
                                }, status=200)
            else:
                return Response({'success': False, 'message': 'Invalid password'})
        except admin.DoesNotExist:
            return Response({'success': False, 'message': 'User not found.'}, status=404)
    else:
        return Response({'error': 'Only POST method are allowed.'}, status=405)