from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from students.models import Students
from main_admin.models import Admins

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = self.get_token_from_header(request)
        if not token:
            return None  # No token provided

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['id']
            user_type = payload['user_type']

            # Try to get the user (either Student or Admin)
            if user_type == 'admin':
                user = Admins.objects.get(id=user_id)

            elif user_type == 'student':
                user = Students.objects.get(id=user_id)
            else:
                raise AuthenticationFailed('User does not exist')
            return (user, token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
        except (Students.DoesNotExist, Admins.DoesNotExist):
            raise AuthenticationFailed('User not found')

    def get_token_from_header(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header and auth_header.startswith('Bearer '):
            return auth_header.split(' ')[1]
        return None
