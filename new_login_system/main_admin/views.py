from django.shortcuts import render
import logging
logger = logging.getLogger(__name__)
from rest_framework import viewsets
from .models import Admins
from .serializers import Admins_serializer
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
# from rest_framework.decorators import api_view

from rest_framework.decorators import action
from django.utils.dateparse import parse_date
# from drf_spectacular.utils import extend_schema

# for show swagger parameter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

from utils.base_viewsets import BaseCRUDViewSet
from utils.base_viewsets import success_response, error_response

def admin_dashboard(request):
    """Admin dashboard page"""
    try:
        return render(request, 'admin-dashboard.html')
    except Exception as e:
        logger.error(f"Error loading admin dashboard: {e}")
        return render(request, 'error.html', {'message': 'Unable to load dashboard'})

def admin_students(request):
    """Admin students management page"""
    try:
        return render(request, 'admin-students.html')
    except Exception as e:
        logger.error(f"Error loading admin students page: {e}")
        return render(request, 'error.html', {'message': 'Unable to load students page'})

def admin_fees(request):
    """Admin fees management page"""
    try:
        return render(request, 'admin-fees.html')
    except Exception as e:
        logger.error(f"Error loading admin fees page: {e}")
        return render(request, 'error.html', {'message': 'Unable to load fees page'})

def admin_attendance(request):
    """Admin attendance management page"""
    try:
        return render(request, 'admin-attendance.html')
    except Exception as e:
        logger.error(f"Error loading admin attendance page: {e}")
        return render(request, 'error.html', {'message': 'Unable to load attendance page'})

def admin_calendar(request):
    """Admin calendar management page"""
    try:
        return render(request, 'admin-calendar.html')
    except Exception as e:
        logger.error(f"Error loading admin calendar page: {e}")
        return render(request, 'error.html', {'message': 'Unable to load calendar page'})

def admin_homework(request):
    """Admin homework management page"""
    try:
        return render(request, 'admin-homework.html')
    except Exception as e:
        logger.error(f"Error loading admin homework page: {e}")
        return render(request, 'error.html', {'message': 'Unable to load homework page'})

def admin_notices(request):
    """Admin notices management page"""
    try:
        return render(request, 'admin-notices.html')
    except Exception as e:
        logger.error(f"Error loading admin notices page: {e}")
        return render(request, 'error.html', {'message': 'Unable to load notices page'})

def admin_calendar(request):
    """Admin calendar management page"""
    try:
        return render(request, 'admin-calendar.html')
    except Exception as e:
        logger.error(f"Error loading admin calendar page: {e}")
        return render(request, 'error.html', {'message': 'Unable to load calendar page'})

def admin_homework(request):
    """Admin homework management page"""
    try:
        return render(request, 'admin-homework.html')
    except Exception as e:
        logger.error(f"Error loading admin homework page: {e}")
        return render(request, 'error.html', {'message': 'Unable to load homework page'})

def admin_notices(request):
    """Admin notices management page"""
    try:
        return render(request, 'admin-notices.html')
    except Exception as e:
        logger.error(f"Error loading admin notices page: {e}")
        return render(request, 'error.html', {'message': 'Unable to load notices page'})
    
    
class AdminViewSet(BaseCRUDViewSet):
    queryset = Admins.objects.all()
    serializer_class = Admins_serializer

    def create(self, request, *args, **kwargs):
        try:
            mutable_data = request.data.copy()
            if 'password' in mutable_data:
                mutable_data['password'] = make_password(mutable_data['password'])
            serializer = self.get_serializer(data = mutable_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return success_response("Record created successfully",
                                    serializer.data,
                                    code=status.HTTP_201_CREATED)
        except Exception as e:
            return error_response(f"Error creating record: {e}")
    
