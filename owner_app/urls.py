from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token    

urlpatterns = [
    path('register/',Registration.as_view(), name='registration'),
    path('login/', obtain_auth_token, name='login'),
    path('turf/', TurfCreate.as_view(), name='turf'),
    path('turf_management/<int:pk>/', TurfManagement.as_view(), name='turf_management'),
    path('book/', TurfBookingView.as_view(), name='book'),
    path('payment/<int:pk>/', PaymentHistory.as_view(), name='payment')

]
