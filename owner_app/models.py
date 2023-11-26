from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Owner(AbstractUser):
    Organization_name = models.CharField(max_length=20)
    Phone_number = models.CharField(max_length=10)
