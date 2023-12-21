from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from user_app.models import *
from admin_app.models import Reward
from user_app.models import Team


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
    reward_points = models.IntegerField(default=0)
    
    
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
    price = models.FloatField(default=0)
    image = models.ImageField(upload_to='image/', null=True) 
    description = models.CharField(max_length=255)
    amenity = models.ManyToManyField('Amenity')
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    ai_rating = models.FloatField(null=True)
    # is_active = models.BooleanField(default=False)

    def __str__(self):
        return f' {self.name} ({self.owner.Organization_name})'  
    
    
# class TurfPriceUpdateModel(models.Model):
#     turf = models.ForeignKey(Turf, on_delete=models.CASCADE)
#     old_price = models.DecimalField(default=0, max_digits=10,decimal_places=2)
#     new_price = models.DecimalField(null=True, max_digits=10,decimal_places=2)
    

PAYMENT_CHOICES = (
        ('Partial_payment', 'Partial_payment'),
        ('Full_payment', 'Full_payment'),
        ('Offline_payment', 'Offline_payment')
    )


class AiTurfBookModel(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    price = models.FloatField()
    turf =  models.ForeignKey(Turf, on_delete=models.SET_NULL, null=True)



class TurfBooking(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    user_name = models.CharField(max_length=55)
    user_mobile = models.CharField(max_length=10)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    price = models.FloatField()
    Payment_type = models.CharField(choices=PAYMENT_CHOICES, default='Offline_payment', max_length=30)
    amount_paid = models.IntegerField(default=300, null=True)
    balance = models.IntegerField()      
    turf = models.ForeignKey(Turf, on_delete=models.SET_NULL, null=True)
    is_match_ended = models.BooleanField(default=False)
    
    def is_match_ended(self):
        now = timezone.now().time()
        return now >= self.end_time

    def __str__(self):
        return f"{self.user_name} - Match Ended: {self.is_match_ended()}"

    class Meta:
        unique_together = ['turf', 'date', 'start_time', 'end_time']
    
    # def save(self,*args, **kwargs):
    #     super().save(*args, **kwargs)
        
    #     if self.is_match_ended():
    #         reward_points = int(0.1 * self.price)
    #         reward_point, created = RewardPointModel.objects.get_or_create(booking=self, defaults={'reward_points': reward_points})
    #         if not created:
    #             reward_point.reward_points = reward_points
    #             reward_point.save()



class PaymentHistoryModel(models.Model):
    turf_booking = models.ForeignKey(TurfBooking, on_delete=models.SET_NULL, null=True)
    turf = models.ForeignKey(Turf, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.user} has booked {self.turf}'
        


class MatchRatingModel(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1_match')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2_match')
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)
    turf_booking = models.ForeignKey(TurfBooking, on_delete=models.CASCADE) 
    remark = models.CharField(max_length=50, null=True)
    date_played = models.DateField()
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE)
    players_data = models.JSONField(null=True, blank=True)

  
    def __str__(self):
        return f"{self.team1} {self.team1_score} : {self.team2} {self.team2_score}"
    

class RewardPointModel(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    booking = models.ForeignKey(TurfBooking, on_delete=models.CASCADE)
    reward_points = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return f'{self.booking.user_name} earned {self.reward_points}'
    
    
class Gallery(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery_images/')
    description = models.CharField(max_length=255)
    
    def __str__(self):
        return self.description    

    
class Profile(models.Model):
    user = models.ForeignKey(Abstract, on_delete=models.CASCADE)
    profile_name = models.CharField(max_length=55, null=True)
    profile_pic = models.ImageField(upload_to='profile_image/', null=True)
    
    # def __str__(self):
    #     return self.user

class UserBookingHistory(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    turf_booked = models.ForeignKey(TurfBooking, on_delete=models.CASCADE)
    
    
class RedeemRewardsModel(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    redeemed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.user} has redeemed {self.reward} on {self.redeemed_date}'


class TurfRating(models.Model):
    turfid = models.ForeignKey(Turf, on_delete=models.CASCADE)
    userid = models.ForeignKey(Abstract, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)
    review = models.CharField(max_length=255)
    
    def __str__(self):
        return f'{self.turfid.name} {self.userid}'
        