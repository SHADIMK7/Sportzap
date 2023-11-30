from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from user_app.models import *
from user_app.models import Customer, Team

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
    # is_active = models.BooleanField(default=False)

    def _str_(self):
        return self.name

PAYMENT_CHOICES = (
        ('Partial_payment', 'Partial_payment'),
        ('Full_payment', 'Full_payment')
    )
class TurfBooking(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    user_name = models.CharField(max_length=55)
    user_mobile = models.CharField(max_length=10)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    price = models.FloatField()
    Payment_type = models.CharField(choices=PAYMENT_CHOICES, default='Partial_payment', max_length=30)
    amount_paid = models.IntegerField(default=300, null=True)
    balance = models.IntegerField()      
    turf = models.ForeignKey(Turf, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user_name

class PaymentHistoryModel(models.Model):
    turf_booking = models.ForeignKey(TurfBooking, on_delete=models.SET_NULL, null=True)
    turf = models.ForeignKey(Turf, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.user.username + "has booked " + self.turf.name 


class MatchModel(models.Model):
    team1 = models.ForeignKey(Team, related_name='team1', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='team2', on_delete=models.CASCADE)
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)
    date_played = models.DateField()


class MatchRatingModel(models.Model):
    match = models.ForeignKey(MatchModel, on_delete=models.CASCADE)
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE)
    remark = models.CharField(max_length=50, null=True)