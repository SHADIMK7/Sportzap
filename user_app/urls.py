from django.urls import path
from . views import *
from rest_framework.authtoken.views import obtain_auth_token    


urlpatterns = [
    path('register/', CustomerRegistrationView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('booking/', BookingView.as_view(), name='booking'),
    # path('turf_display/', TurfDisplayView.as_view(), name='turf_display'),
    path('team_list/', TeamView.as_view(), name='team_list'),
    path('team_list/<int:name>/', TeamDetailView.as_view(), name='team_detail'),
    path('player/', PlayerView.as_view(), name='player'),
    path('player_details/<str:name>/', PlayerDetail.as_view(), name='player_detail'),
    path('rewards/<int:pk>/', RewardPoints.as_view(), name='rewards'),
    path('player/<int:name>/', PlayerDetail.as_view(), name='player_detail'),
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('send_invitation/', SendInvitationView.as_view(), name='send_invitation'),
    path('accept_invitation/<int:pk>/', AcceptInvitationView.as_view(), name='accept_invitation'),


    
    ]
    path('booking-history/<int:pk>/', UserBookingHistoryView.as_view(), name="booking-history"),
    path('redeem-rewards/<int:pk>/', RedeemRewards.as_view(), name='redeem-rewards')
]
