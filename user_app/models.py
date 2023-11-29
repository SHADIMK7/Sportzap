from django.db import models
from django.contrib.auth.models import User
from Backend import settings
from owner_app.models import *
from django.contrib.auth.models import AbstractUser,Group,Permission

# from owner_app.models import Turf

# Create your models here.
class Customer(AbstractUser):
    customer_mobile = models.CharField(max_length=10)
    groups = models.ManyToManyField(Group, related_name='customer_groups', null=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customer_user_permissions', null=True)
    
    def __str__(self):
        return self.username
    

    
    
    