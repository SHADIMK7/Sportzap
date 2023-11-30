from django.urls import path
from .views import *

urlpatterns = [
        path('owner_list/',OwnerList.as_view(), name='owner_list'),
        path('owner_list/<int:id>/',OwnerDelete.as_view(), name='owner_list'),
        path('turf_list/',TurfList.as_view(), name='turf_list'),
        path('turf_list/<int:id>/',TurfActiveDelete.as_view(), name='turf_list'),
        path('customer_list/',CustomerList.as_view(), name='customer_list'),
        path('booking_list/',TurfBookingView.as_view(), name='booking_list'),
        # path('admin_view/',AdminDataView.as_view(), name='admin_view'),
        path('customer_list/<int:id>/',CustomerListDelete.as_view(), name='customer_list'),


]
