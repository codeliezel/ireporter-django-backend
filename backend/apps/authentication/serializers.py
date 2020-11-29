from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import User

class AuthSerializer(serializers.ModelSerializer):
    full_names = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Your full names are required.',
        }
    )
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
            )
        ],
        error_messages={
            'required': 'Your email address is required.',
        }
    )
    username = serializers.RegexField(
        regex='^(?!.*\ )[A-Za-z\d\-\_]+$',
        min_length=4,
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Username must be unique',
            )
        ],
        error_messages={
            'invalid': 'Username cannot have a space',
            'required': 'Username is required',
            'min_length': 'Username must have at least 4 characters'
        }
    )
    password = serializers.RegexField(
        regex="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
        max_length=20,
        min_length=8,
        write_only=True,
        required=True,
        error_messages={
            'required': 'Password is required',
            'invalid': 'Password must have a number and a letter',
            'min_length': 'Password must have at least 8 characters',
            'max_length': 'Password cannot be more than 128 characters'
        }
    )

    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['full_names', 'email', 'username', 'password', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    full_names = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'Please, supply an email address.'
            )

        if password is None:
            raise serializers.ValidationError(
                'Please, supply the password.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        return {
            'full_names': user.full_names,
            'email': user.email,
            'username': user.username,
            'token': user.token,
        }
                