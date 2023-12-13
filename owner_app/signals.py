from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import TurfBooking, RewardPointModel, PaymentHistoryModel, UserBookingHistory, Customer, AiTurfBookModel
from django.db import transaction
from django.db.utils import IntegrityError


@receiver(post_save, sender=AiTurfBookModel)
def create_date_and_time(sender, instance, created, **kwargs):
    if created and not hasattr(instance, '_being_tested'):
        print("STARTED AI TURF BOOKING")
        try:
            TurfBooking.objects.create(
                user=instance.user,
                date=instance.date,
                start_time=instance.start_time,
                end_time=instance.end_time,
                price=instance.price,
                turf = instance.turf
            )
        except IntegrityError as e:
            print(f"Error creating TurfBooking: {str(e)}")


@receiver(pre_save, sender = TurfBooking )
def create_balance(sender, instance , **kwargs):
    print("BALANCE STARTED")
    if instance.Payment_type != 'Offline':
        instance.balance = instance.price - instance.amount_paid
    else:
        instance.balance = instance.price
        instance.amount_paid = instance.price

  
@receiver(post_save, sender=TurfBooking)
def add_reward_points(sender, instance, **kwargs):
    print("reward started")
    
    if instance.is_match_ended() and instance.user and isinstance(instance.user, Customer):
        reward_points = int(0.1 * instance.price)
        
        customer = instance.user
        print("customer before:", customer.reward_points)
        
        customer.reward_points += reward_points
        customer.save()
        print("customer after:", customer.reward_points)

        RewardPointModel.objects.create(user=instance.user, booking=instance, reward_points=reward_points)
        

        
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

# @receiver(post_save, sender=Turf)
# def update_turf_price(sender, instance, **kwargs):
#     if not kwargs.get('created'):
#         TurfPriceUpdateModel.objects.create(
#             turf = instance,
#             old_price = instance.price
#         )
#         print("NOT KWARGS")
#         if instance.price != TurfPriceUpdateModel.new_price:
#             TurfPriceUpdateModel.objects.create(
#                 turf = instance,
#                 old_price = instance.price,
#                 new_price = instance.price                
#             )
#             print("2nd if ")