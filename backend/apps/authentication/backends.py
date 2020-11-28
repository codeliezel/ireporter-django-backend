import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User

class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        token = authentication.get_authorization_header(request)
     
        if not token:
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            raise AuthenticationFailed('Invalid token.')

        try:
            user = User.objects.get(id=payload['id'])
        except User.DoesNotExist:
            raise AuthenticationFailed('No user found for token provided')

        return (user, token)