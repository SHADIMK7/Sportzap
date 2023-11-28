from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission

# Create your models here.
class Owner(AbstractUser):
    Organization_name = models.CharField(max_length=20)
    Phone_number = models.CharField(max_length=10)
    groups = models.ManyToManyField(Group, related_name='owner_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='owner_user_permissions')
