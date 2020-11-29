import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models

class UserManager(BaseUserManager):

    def create_user(self, full_names, username, email, password):
        if full_names is None:
            raise TypeError('Your full names please.')

        if username is None:
            raise TypeError('No username supplied.')

        if email is None:
            raise TypeError('An email address is required.')

        if password is None:
            raise TypeError('Include your password.')    

        user = self.model(full_names=full_names, username=username, 
        email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, full_names, username, email, password):
      if password is None:
          raise ValueError('As a superuser, you must have a password.')

      user = self.create_user(full_names, username, email, password)
      user.is_superuser = True
      user.save()

      return user

class User(AbstractBaseUser, PermissionsMixin):
    full_names = models.CharField(max_length=25)
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.username

    def get_long_name(self):
        return self.full_names  
  
    def token(self):

        dt = datetime.now() + timedelta(days=7)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')