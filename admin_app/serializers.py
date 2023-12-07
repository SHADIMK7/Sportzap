from rest_framework import serializers
from owner_app.models import *
from user_app.models import *
from django.contrib.auth import get_user_model
from admin_app.models import Leaderboard,Reward


class TurfSerializer(serializers.ModelSerializer):

    class Meta:
        model = Turf
        fields = '__all__'



class AbstractUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Abstract
        fields = ['first_name','last_name','email','phone_no']


class OwnerSerializer(serializers.ModelSerializer):

    # abstract_user_details = AbstractUserSerializer(source='abstract', read_only=True)
    turf = serializers.SerializerMethodField()
    name = serializers.StringRelatedField(source='abstract.first_name')
    email = serializers.StringRelatedField(source='abstract.email')
    phone = serializers.StringRelatedField(source='abstract.phone_no')
    class Meta:
        model = Owner
        fields = ['id',  'turf','Organization_name','name','email','phone',  'turf']

    def get_turf(self, owner):
        turfs = owner.turf_set.all()
        turf_serializer = TurfSerializer(turfs, many=True)
        return turf_serializer.data

class CustomerListSerializer(serializers.ModelSerializer):

    abstract_user_details = AbstractUserSerializer(source='customer', read_only=True)
    booking_count = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['id', 'abstract_user_details', 'booking_count','customer_name']
    def get_booking_count(self, customer):
        booking_count = TurfBooking.objects.filter(user=customer).count()
        return booking_count
    
    
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurfBooking
        fields = '__all__'

class TransactionHistorySerializer(serializers.ModelSerializer):
    user_name = serializers.StringRelatedField(source='user.first_name')
    turf_name = serializers.StringRelatedField(source='turf.name')
    price = serializers.StringRelatedField(source="turf_booking.price")
    amount_paid = serializers.StringRelatedField(source="turf_booking.amount_paid" )
    balance = serializers.StringRelatedField(source = "turf_booking.balance")
    amount_credited_to_admin = serializers.SerializerMethodField()
    amount_credited_to_turf = serializers.SerializerMethodField()

    class Meta:
        model = PaymentHistoryModel
        fields = ['id', 'turf_booking', 'turf_name', 'user_name','amount_paid','price','balance','amount_credited_to_admin','amount_credited_to_turf'] 

    def get_amount_credited_to_admin(self, obj):
        turf_price = obj.turf_booking.price
        amount_credited_to_admin = turf_price * 0.20
        return amount_credited_to_admin

    def get_amount_credited_to_turf(self, obj):
        amount_credited_to_admin = self.get_amount_credited_to_admin(obj)
        amount_paid_to_turf =obj.turf_booking.amount_paid
        amount_credited_to_turf =  amount_paid_to_turf - amount_credited_to_admin
        return amount_credited_to_turf


class TurfUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only='True')

    name = serializers.CharField(read_only='True')
    location = serializers.CharField(read_only='True')
    price = serializers.BooleanField(read_only='True')
    image = serializers.ImageField(read_only='True')
    description = serializers.CharField(read_only='True')
    amenity = serializers.CharField(read_only='True')
    is_active = serializers.BooleanField(default=False)

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

# class LeaderBoardSerializer(serializers.ModelSerializer):
#     team_details1 = TeamSerializer(source='team1', read_only=True)
#     team_details2 = TeamSerializer(source='team2', read_only=True)

#     class Meta:
#         model = MatchRatingModel
#         fields = '__all__'

class LeaderBoardSerializer(serializers.ModelSerializer):
   
    
    class Meta:
        model = Leaderboard
        fields = '__all__'

class PlayerLeaderBoardSerializer(serializers.ModelSerializer):    
    team_name = serializers.StringRelatedField(source= "team.team_name")
    no_of_win = serializers.SerializerMethodField()
    class Meta:
        model = Player
        fields = ['player_name','player_pic','player_position','team','no_of_win','team_name']   

    def get_no_of_win(self, instance):
        try:
            leaderboard = Leaderboard.objects.get(team=instance.team)
            return leaderboard.number_of_wins
        except Leaderboard.DoesNotExist:
            return 0

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'

class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'        