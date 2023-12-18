import uuid
from django.db import models
from django.contrib.auth.models import User
from owner_app.models import *
from django.contrib.auth.models import AbstractUser

# Create your models here.
# class Customer(AbstractUser):
#     customer_mobile = models.CharField(max_length=10)
#     customer_latitude = models.FloatField(null=True)
#     customer_longitude = models.FloatField(null=True)

    
#     def __str__(self):
#         return self.username

SKILL_CHOICES = (
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Professional', 'Professional')
)
    
class Team(models.Model):
    team_name = models.CharField(max_length=55)
    team_skill = models.CharField(choices=SKILL_CHOICES, default='Beginner', max_length=20)
    team_pic = models.ImageField(upload_to='team_image/', null=True)
    team_strength = models.IntegerField()
    team_longitude = models.FloatField(null=True)
    team_latitude = models.FloatField(null=True)
    
    def __str__(self):
        return self.team_name
    
class Player(models.Model):
    # player_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    player_name = models.CharField(max_length=55)
    player_skill = models.CharField(choices=SKILL_CHOICES, default='Beginner', max_length=20)
    player_pic = models.ImageField(upload_to='player_image/', null=True)
    player_position = models.CharField(max_length=10)
    teams = models.ManyToManyField('Team', related_name='players')
    invitation_pending = models.BooleanField(default=False) 
    player_longitude = models.FloatField(null=True)
    player_latitude = models.FloatField(null=True)
    
    
    def __str__(self):
        return self.player_name
    
class TeamInvitation(models.Model):
    team = models.ForeignKey('Team', related_name='invitations', on_delete=models.CASCADE)
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.team} {self.player}"
    
    
class MatchInvitation(models.Model):
    sender_team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='sender')
    receiver_team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='receiver')
    is_accepted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.sender_team} {self.receiver_team}"
    

# class RewardPoints(models.Model):
#     user = models.ForeignKey(Customer,on_delete=models.CASCADE)
   
class Charge(models.Model):
    amount = models.IntegerField()
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=20)
    stripe_charge_id = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Add other fields as needed

    def __str__(self):
        return f"{self.amount} {self.currency} - {self.stripe_charge_id}" 