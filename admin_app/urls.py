from django.urls import path
from .views import *

urlpatterns = [
        path('admin_income/',AdminIncomeView.as_view(),name='admin_income'),
        path('owner_list/',OwnerList.as_view(), name='owner_list'),
        path('owner_list/<int:pk>/',OwnerDelete.as_view(), name='owner_list'),
        path('turf_list/',TurfList.as_view(), name='turf_list'),
        path('turf_list/<int:pk>/',TurfActiveDelete.as_view(), name='turf_list'),
        path('customer_list/',CustomerList.as_view(), name='customer_list'),
        path('booking_list/',TurfBookingView.as_view(), name='booking_list'),
        # path('admin_view/',AdminDataView.as_view(), name='admin_view'),
        path('customer_list/<int:pk>/',CustomerListDelete.as_view(), name='customer_list'),
        path('booking_list/<int:pk>/',TurfBookingCancel.as_view(), name='booking_list'),
        path('transaction_list/',TransactionHistory.as_view(), name='transaction_list')

]
