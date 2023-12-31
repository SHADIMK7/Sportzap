from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import TurfBooking, RewardPointModel, PaymentHistoryModel, UserBookingHistory, Customer, AiTurfBookModel, RedeemRewardsModel
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
    # print("BALANCE STARTED")
    instance.balance = 0
    instance.amount_paid = instance.price
    # print("BALANCE TYPE NOT OFFLINE", instance.balance)
    # else:
    #     instance.balance = 0
    #     print("BALANCE TYPE OFFLINE", instance.balance)
        
# @receiver(pre_save, sender = TurfBooking)
# def create_username(self, request, sender, instance, **kwargs):
#     print("user started")
#     TurfBooking.objects.create(
#         user_name = request.user.username,
#         user_mobile = request.user.phone_no
#     )

  
@receiver(post_save, sender=TurfBooking)
def add_reward_points(sender, instance, **kwargs):
    # print("reward started")
    
    if instance.is_match_ended() and instance.user and isinstance(instance.user, Customer):
        reward_points = int(0.1 * instance.price)
        
        customer = instance.user
        # print("customer before:", customer.reward_points)
        
        customer.reward_points += reward_points
        customer.save()
        # print("customer after:", customer.reward_points)

        RewardPointModel.objects.create(user=instance.user, booking=instance, reward_points=reward_points)
        

        
# @receiver(post_save, sender=TurfBooking)
# def create_payment_history(sender, instance, created, **kwargs):
#     # print("Payment history")
#     if created:
#         PaymentHistoryModel.objects.create(
#             turf_booking=instance,
#             turf=instance.turf,
#             user=instance.user
#         )
        
        
        
@receiver(post_save, sender=TurfBooking)
def create_payment_history(sender, instance, created, **kwargs):
    # print("PAYMENT history STARTED")
    if created:
        # print("IF CREATED:")
        # print("INSTANCE", instance)
        # print("turf id ", instance.turf.id)
        # print("date", instance.date)
        PaymentHistoryModel.objects.create(
            turf_id = instance.turf.id,
            turf_name = instance.turf.name,
            user_id = instance.user.id,
            username = instance.user.customer.username,
            turf_price = instance.price,
            date_booked = instance.date,
            start_time = instance.start_time,
            end_time = instance.end_time
        )
        # print("PAYMENT HISTORY MODEL", "turf_id : ", instance.turf,"turf_name : ",instance.turf.name,"user_id : ",instance.user.id,"username : ",instance.user.customer.username,"price : ",instance.price,"date_booked : ",instance.date,"start_time : ",instance.start_time,"end_time : ",instance.end_time)
        
@receiver(post_save,sender = TurfBooking)
def create_user_booking_history(sender, instance, created, **kwargs):
    # print("USER BOOKING HISTORY")
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