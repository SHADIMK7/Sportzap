from django.urls import path
from . views import *

urlpatterns = [
    path('register/', CustomerRegistrationView.as_view(), name='register'),
]
