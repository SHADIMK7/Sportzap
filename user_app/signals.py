from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from owner_app.models import *


# @receiver(post_save, sender=Abstract)
# def create_profile(sender, instance, created, **kwargs):
#     print('HI')
#     if instance.usertype == "customer":
#         Profile.objects.create(
#             user = instance,
#             email = instance.email,
#             phone_no = instance.phone_no
#         )

