from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission

# Create your models here.
class Customer(AbstractUser):
    customer_mobile = models.CharField(max_length=10)
    groups = models.ManyToManyField(Group, related_name='customer_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='customer_user_permissions')
    
    def __str__(self):
        return self.customer_mobile
    