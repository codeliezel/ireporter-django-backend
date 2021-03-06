from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from rest_framework.permissions import AllowAny
from .serializers import (AuthSerializer, LoginSerializer)
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
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class LoginView(APIView):
    """
    Sign in a user
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)        