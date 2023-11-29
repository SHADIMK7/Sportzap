from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from user_app.models import *

# Create your models here.
class Owner(AbstractUser):
    Organization_name = models.CharField(max_length=20)
    Phone_number = models.CharField(max_length=10)


class Amenity(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='amenity_icon')
    
    def _str_(self):
        return self.name
    
class Turf(models.Model):
    name = models.CharField(max_length=55)
    location = models.CharField(max_length=55)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='image/') 
    description = models.CharField(max_length=255)
    amenity = models.ManyToManyField(Amenity)

    def _str_(self):
        return self.name
    
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
