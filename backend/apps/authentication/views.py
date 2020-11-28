from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from rest_framework.permissions import AllowAny
from .serializers import AuthSerializer
from django.conf import settings

class AuthView(APIView):
    """
    Sign up a user
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        serializer = AuthSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        # # configure email
        # user_email = data['email']
        # subject = 'Welcome to Rachis.io'
        # message = 'I\'m sure you will find what you like. Yay!'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [user_email,]

        # send_mail( subject, message, email_from, recipient_list )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)