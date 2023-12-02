from django.db import models
from django.contrib.auth.models import AbstractUser
from user_app.models import *
# from user_app.models import Customer, Team

# Create your models here.

TYPE_CHOICES = (
    ('owner' , 'owner'),
    ('customer' , 'customer')
)

class Abstract(AbstractUser):
    phone_no = models.CharField(max_length=10)
    usertype = models.CharField(choices=TYPE_CHOICES, default='customer' ,max_length=30)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    
    def __str__(self):
        return self.username
    
class Owner(models.Model):
    abstract = models.ForeignKey(Abstract, on_delete=models.CASCADE)
    Organization_name = models.CharField(max_length=20)
    
    def __str__(self) :
        return f' {self.Organization_name} ({self.abstract.username})' 
    
class Customer(models.Model):
    customer = models.ForeignKey(Abstract, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.customer_name


class Amenity(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='amenity_icon')
    
    def __str__(self):
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

    def __str__(self):
        return f' {self.name} ({self.owner.Organization_name})'  

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


class MatchRatingModel(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1_match')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2_match')
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)
    date_played = models.DateField()
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE)
    remark = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return f"{self.team1} {self.team1_score} : {self.team2} {self.team2_score}"