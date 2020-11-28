from django.urls import path, include
                      
urlpatterns = [
    path('api/', include(('backend.apps.authentication.urls'), namespace='auth'))
]