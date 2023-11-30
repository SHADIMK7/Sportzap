from django.db import models
from django.contrib.auth.models import User
from owner_app.models import *
from django.contrib.auth.models import AbstractUser

# from owner_app.models import Turf

# Create your models here.
class Customer(AbstractUser):
    customer_mobile = models.CharField(max_length=10)
<<<<<<< HEAD
=======
    customer_latitude = models.FloatField()
    customer_longitude = models.FloatField()
>>>>>>> 1d90408afba53a3c13e8c0b9dca6ec00598f651c
    groups = models.ManyToManyField('auth.Group')
    user_permissions = models.ManyToManyField('auth.Permission')
    
    def __str__(self):
        return self.username
    
class Player(models.Model):
    player_name = models.CharField(max_length=55)
    player_photo = models.ImageField(upload_to='player_image/')
    player_position = models.CharField(max_length=10)
    
class Team(models.Model):
    player = models.ManyToManyField(Player)
    team_name = models.CharField(max_length=55)
    team_strength = models.IntegerField()
    team_longitude = models.FloatField()
    team_latitude = models.FloatField()
    

    
    
    