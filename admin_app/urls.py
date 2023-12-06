from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

urlpatterns = [
        path('login/',obtain_auth_token, name='login'),

        path('admin_income/',AdminIncomeView.as_view(),name='admin_income'),
        path('owner_list/',OwnerList.as_view(), name='owner_list'),
        path('owner_retrieve_delete/<int:pk>/',OwnerRetrieveDelete.as_view(), name='owner_retrieve_delete'),
        path('turf_list/',TurfList.as_view(), name='turf_list'),
        path('turf_retrieve_delete/<int:pk>/',TurfActiveDelete.as_view(), name='turf_retrieve_delete'),
        path('customer_list/',CustomerList.as_view(), name='customer_list'),
        path('customer_retrieve_delete/<int:pk>/',CustomerListDelete.as_view(), name='customer_retrieve_delete'),
        path('booking_list/',TurfBookingView.as_view(), name='booking_list'),
        path('booking_cancel/<int:pk>/',TurfBookingCancel.as_view(), name='booking_cancel'),
        # path('admin_view/',AdminDataView.as_view(), name='admin_view'),
        path('transaction_list/',TransactionHistory.as_view(), name='transaction_list'),
        # path('logout/',LogoutView.as_view(), name='logout')
        path('leader_board/',LeaderBoard.as_view(),name='leader_board'),
        path('player_leader_board/',PlayerLeaderBoard.as_view(),name='player_leaderboard'),
        path('amenity/',AmenityView.as_view(),name='amenity'),
        path('amenity_delete/<int:pk>/',AmenityDelete.as_view(),name='amenity_delete'),
        path('reward_create_list/',RewardView.as_view(),name='reward_create_list'),
        path('reward_update_delete/<int:pk>/',RewardUpdateDelete.as_view(),name='reward_update_delete')
]
