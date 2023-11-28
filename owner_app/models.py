from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission

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
    turf_name = models.CharField(max_length=55)
    turf_location = models.CharField(max_length=55)
    turf_price = models.DecimalField(max_digits=10, decimal_places=2)
    turfcourt_image = models.ImageField(upload_to='image/') 
    turf_description = models.CharField(max_length=255)
    turf_amenity = models.ManyToManyField(Amenity)
        
    def _str_(self):
        return self.turf_name
