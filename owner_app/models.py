from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
# from user_app.models import TurfBooking

# Create your models here.
class Owner(AbstractUser):
    Organization_name = models.CharField(max_length=20)
    phone_no = models.CharField(max_length=10)


class Amenity(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='amenity_icon')
    
    def _str_(self):
        return self.name
    
class Turf(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    name = models.CharField(max_length=55)
    location = models.CharField(max_length=55)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='image/') 
    description = models.CharField(max_length=255)
    amenity = models.ManyToManyField(Amenity)

    def _str_(self):
        return self.name


# class PaymentHistory(models.Model):
#     turf_booking = models.ForeignKey(TurfBooking, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Payment for user {self.user.username} on {self.date_added}"