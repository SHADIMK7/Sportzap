from rest_framework import serializers
from . models import *
from owner_app . models import *
from django.contrib.auth import get_user_model


class AbstractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Abstract
        fields  = ['username', 'email', 'password' , 'phone_no']
        extra_kwargs = {
            'email': {'required': True},
        }
        
        def create(self, validated_data):
            validated_data = {
                'username': validated_data['username'],
                'email': validated_data['email'],
                'phone_no': validated_data['phone_no'], 
                'usertype': 'customer'
            }
            abstract = Abstract.objects.create(**validated_data)
            abstract.set_password(validated_data['password'])
            abstract.save()
            return abstract

class RegisterUserSerializer(serializers.ModelSerializer):
    abstract = AbstractSerializer()
        
    class Meta:
        model = Customer
        fields = ['abstract']
            
    def create(self, validated_data):
        abstract_data = validated_data.pop('abstract')
        password = abstract_data.get('password')
        customer = abstract_data.get('username')
        abstract = AbstractSerializer(data=abstract_data)
        if abstract.is_valid():
            abstract = abstract.save()
            
            abstract.set_password(password)
            abstract.save()
            account = Customer.objects.create(customer=abstract, **validated_data, customer_name = customer)
            return account
        else:
            raise serializers.ValidationError({"abstract": abstract.errors})
    
class TurfBookingSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()
    class Meta:
        model = TurfBooking  
        fields = "__all__"

    def get_balance(self,object):
        return object.price - object.amount_paid
        
class TurfDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Turf
        fields = '__all__'
        
class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['player_name', 'player_skill', 'player_pic', 'player_position']

        
class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, required=False, read_only=True)
    
    class Meta:
        model = Team
        fields = '__all__'
        
class TeamInvitationSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamInvitation
        fields = '__all__'
        
    # def create(self, validated_data):
    #     players_data = validated_data.pop('players', [])

    #     # Assuming you have a Team model with a proper creation logic
    #     team_instance = Team.objects.create(**validated_data)

    #     for player_data in players_data:
    #         Player.objects.create(team=team_instance, **player_data)

    #     return team_instance
        
    # def update(self, instance, validated_data):
    #     players_data = validated_data.pop('players', [])
    #     max_players = instance.team_strength if instance else self.Meta.model.team_strength_limit
    #     if len(instance.players.all()) + len(players_data) > max_players:
    #         raise serializers.ValidationError(f'Team can have at most {max_players} players.')
    #     instance = super().update(instance, validated_data)

    #     for player_data in players_data:
    #         player_instance = instance.players.filter(id=player_data.get('id')).first()
    #         if player_instance:
    #             PlayerSerializer().update(player_instance, player_data)
    #         else:
    #             instance.players.create(**player_data)
    #     return instance
    
    
class RewardPointSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField
    # reward_points = serializers.SerializerMethodField
    
    class Meta:
        model = RewardPointModel
        fields = ['user' ,'booking', 'reward_points']
        
    # def get_user(self,request):
    #     return self.booking.user
    
    # def get_reward_points(self,request):
    #     if self.booking.is_match_ended == "True":
    #         reward_points = reward_points + 10/100 * (self.booking.price)
    #         return reward_points
    
    
class UserBookingHistorySerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    date_booked = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    amount_paid = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()
    
    class Meta:
        model = UserBookingHistory
        fields = ['user', 'turf_booked', 'user_name', 'date_booked', 'price','amount_paid', 'balance']
        
    def get_user_name(self,object):
        return object.user.customer_name    
    
    def get_date_booked(self,object):
        return object.turf_booked.date
    
    def get_price(self,object):
        return object.turf_booked.price
    
    def get_amount_paid(self,object):
        return object.turf_booked.amount_paid
    
    def get_balance(self,object):
        return object.turf_booked.balance
    
    

# class RedeemRewardsSerializer(serializers.ModelSerializer):
#     required_points = serializers.SerializerMethodField()
    
#     class Meta:
#         model = RedeemRewardsModel
#         fields = ['user', 'required_points', 'reward']
    
#     def get_required_points(self, object):
#         # Check if 'object' is an instance of RedeemRewardsModel
#         if isinstance(object, RedeemRewardsModel):
#             return object.reward.reward_points
#         # Check if 'object' is an instance of dict
#         elif isinstance(object, dict) and 'reward' in object:
#             # Handle the case when 'object' is a dictionary with 'reward'
#             return object['reward'].reward_points
#         return None 

# class UserReviewSerializer(serializers.ModelSerializer):
#     user = serializers.SerializerMethodField()

#     class Meta:
#         model = UserReviewModel
#         fields = ['user', 'review', 'sentiment']

#     def get_user(self, obj):
#         return obj.user.id
    
    
class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'
  
  
        
User = get_user_model()      
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_no', 'email']
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_name', 'profile_pic']
        
class ProfileCombinedSerializer(serializers.Serializer):
    abstract = UserProfileSerializer()
    profile = ProfileSerializer()
    