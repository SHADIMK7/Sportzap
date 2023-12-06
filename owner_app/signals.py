from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import TurfBooking, RewardPointModel, PaymentHistoryModel, UserBookingHistory


@receiver(pre_save, sender = TurfBooking )
def create_balance(sender, instance , **kwargs):
    print("BALANCE STARTED")
    instance.balance = instance.price - instance.amount_paid
    
    
# "http://1800:/analyse"

# response 


  
@receiver(post_save, sender=TurfBooking)
def add_reward_points(sender, instance, **kwargs):
    print("reward started")
    if instance.is_match_ended():
        reward_points = int(0.1 * instance.price)
        RewardPointModel.objects.create(booking=instance, reward_points=reward_points)
        
        
@receiver(post_save, sender=TurfBooking)
def create_payment_history(sender, instance, created, **kwargs):
    print("Payment history")
    if created:
        PaymentHistoryModel.objects.create(
            turf_booking=instance,
            turf=instance.turf,
            user=instance.user
        )
        
        
@receiver(post_save,sender = TurfBooking)
def create_user_booking_history(sender, instance, created, **kwargs):
    print("USER BOOKING HISTORY")
    if created:
        UserBookingHistory.objects.create(
            turf_booked = instance,
            user = instance.user
        )
