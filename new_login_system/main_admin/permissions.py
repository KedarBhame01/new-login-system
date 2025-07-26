# main_admin/permissions.py

from rest_framework.permissions import BasePermission
from .models import Admins  # Import your Admins model

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to perform write operations.
    Students (or any other authenticated user) can only perform read operations.
    """
    def has_permission(self, request, view):
        # Rule 1: Allow any authenticated user to view data (read-only access).
        # The 'GET', 'HEAD', 'OPTIONS' methods are considered "safe".
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Rule 2: For any other method (like POST, PUT, DELETE),
        # only allow it if the user is an instance of the Admins model.
        # Your JWTAuthentication class sets request.user for us.
        return request.user and isinstance(request.user, Admins)
