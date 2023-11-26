from django.urls import path
from .views import *

urlpatterns = [
         path('turf_list/',TurfList.as_view(), name='turf_list'),

]
