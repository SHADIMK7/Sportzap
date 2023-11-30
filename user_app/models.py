from django.db import models
from django.contrib.auth.models import User
from Backend import settings
from owner_app.models import *
from django.contrib.auth.models import AbstractUser,Group,Permission

# from owner_app.models import Turf

# Create your models here.
class Customer(AbstractUser):
    customer_mobile = models.CharField(max_length=10)
    groups = models.ManyToManyField('auth.Group')
    user_permissions = models.ManyToManyField('auth.Permission')
    
    def __str__(self):
        return self.username
    

    
    
    