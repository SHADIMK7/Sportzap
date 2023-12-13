from django.urls import path
from .views import *
# from rest_framework.authtoken.views import obtain_auth_token    

urlpatterns = [
    path('register/',Registration.as_view(), name='registration'),
    # path('login/', CustomLoginView.as_view(), name='custom-login'),
    path('turf/<int:pk>/', TurfCreate.as_view(), name='turf'),
    path('turf_management/<int:pk>/', TurfManagement.as_view(), name='turf_management'),
    path('payment/<int:pk>/', PaymentHistory.as_view(), name='payment'),
    path('match_rating/<int:pk>/', MatchRating.as_view(), name='match_rating'),
    path('turf-display/<int:pk>/', TurfDisplay.as_view(), name='turf-display')

]
