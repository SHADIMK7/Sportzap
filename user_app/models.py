from django.db import models
from django.contrib.auth.models import User
from Backend import settings
from owner_app.models import *
from django.contrib.auth.models import AbstractUser,Group,Permission

# Create your models here.
class Customer(AbstractUser):
    customer_mobile = models.CharField(max_length=10)
    groups = models.ManyToManyField(Group, related_name='customer_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='customer_user_permissions')
    
    def __str__(self):
        return self.username
    
class TurfBooking(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    user_name = models.CharField(max_length=55)
    user_mobile = models.CharField(max_length=10)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    price = models.FloatField()
    payment_method = models.CharField(max_length=10)
    turf = models.ForeignKey(Turf, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.user_name
    
    
    