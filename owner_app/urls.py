from django.urls import path
from .views import *


urlpatterns = [
    path('register/',Registration.as_view(), name='registration'),
    path('turf/<int:pk>/', TurfCreate.as_view(), name='turf'),
    path('turf_management/<int:pk>/', TurfManagement.as_view(), name='turf_management'),
    path('payment/<int:pk>/', PaymentHistory.as_view(), name='payment'),
    path('match_rating/<int:pk>/', MatchRating.as_view(), name='match_rating'),
    path('turf-display/<int:pk>/', TurfDisplay.as_view(), name='turf-display'),
    path('turf-display-all/', TurfDisplayAll.as_view(), name='turf-display-all'),
    path('amenity/', AmenityView.as_view(), name='amenity'),
    path('owner_delete/', OwnerDelete.as_view(), name="owner_delete"),
    path('change-password/', ChangePasswordOwner.as_view(), name="change-password")


]
