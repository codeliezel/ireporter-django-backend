from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (AuthView, LoginView)

app_name = 'auth'

urlpatterns = [
    path('users/signup', AuthView.as_view(), name='user_sign_up'),
    path('users/signin', LoginView.as_view(), name='user_sign_in'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
