from django.db import models
from django.contrib.auth.models import User
from owner_app.models import *
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Customer(AbstractUser):
    customer_mobile = models.CharField(max_length=10)
    customer_latitude = models.FloatField()
    customer_longitude = models.FloatField()
    groups = models.ManyToManyField('auth.Group')
    user_permissions = models.ManyToManyField('auth.Permission')
    
    def __str__(self):
        return self.username
    
class Team(models.Model):
    team_name = models.CharField(max_length=55)
    team_pic = models.ImageField(upload_to='team_image/')
    team_strength = models.IntegerField()
    team_longitude = models.FloatField()
    team_latitude = models.FloatField()
    
    def __str__(self):
        return self.team_name
    
class Player(models.Model):
    player_name = models.CharField(max_length=55)
    player_pic = models.ImageField(upload_to='player_image/')
    player_position = models.CharField(max_length=10)
    team = models.ForeignKey('Team', related_name='players', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.player_name
    