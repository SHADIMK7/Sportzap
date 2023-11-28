from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token    

urlpatterns = [
    path('register/',Registration.as_view(), name='registration'),
    path('login/', obtain_auth_token, name='login'),
    path('turf/', TurfCreate.as_view(), name='turf'),
    path('turf_management/<int:id>/', TurfManagement.as_view(), name='turf_management'),

]
