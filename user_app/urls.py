from django.urls import path
from . views import *

urlpatterns = [
    path('register/', CustomerRegistrationView.as_view(), name='register'),
    path('booking/', BookingView.as_view(), name='booking'),
    path('turf_display/', TurfDisplayView.as_view(), name='turf_display'),
]
