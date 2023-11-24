from django.urls import path
from .views import *

urlpatterns = [
    path('',Registration.as_view(), name='registration'),

]
