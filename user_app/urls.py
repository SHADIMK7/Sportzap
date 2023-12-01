from django.urls import path
from . views import *

urlpatterns = [
    path('register/', CustomerRegistrationView.as_view(), name='register'),
    path('booking/', BookingView.as_view(), name='booking'),
    path('turf_display/', TurfDisplayView.as_view(), name='turf_display'),
    path('team_list/', TeamView.as_view(), name='team_list'),
    path('team_detail/<int:name>/', TeamDetailView.as_view(), name='team_detail'),
    path('player/', PlayerView.as_view(), name='player'),
    path('player_details/<str:name>/', PlayerDetail.as_view(), name='player_detail'),
]
