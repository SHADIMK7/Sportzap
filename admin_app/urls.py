from django.urls import path
from .views import *

urlpatterns = [
        path('owner_list/',OwnerList.as_view(), name='owner_list'),
        path('owner_list/<str:username>/',OwnerDelete.as_view(), name='owner_list'),
        path('turf_list/',TurfList.as_view(), name='turf_list'),
        path('turf_list/<str:username>/',TurfDelete.as_view(), name='turf_list'),


]
