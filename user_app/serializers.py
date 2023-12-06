from rest_framework import serializers
from . models import *
from owner_app . models import *

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
        fields = '__all__'

        
class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True)
    
    class Meta:
        model = Team
        fields = '__all__'
        
    def update(self, instance, validated_data):
        players_data = validated_data.pop('players', [])
        instance = super().update(instance, validated_data)

        for player_data in players_data:
            print('working')
            player_instance = instance.players.filter(id=player_data.get('id')).first()
            if player_instance:
                PlayerSerializer().update(player_instance, player_data)
            else:
                instance.players.create(**player_data)

        return instance
    
    
class RewardPointSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField
    reward_points = serializers.SerializerMethodField
    
    class Meta:
        model = RewardPointModel
        fields = ['booking', 'reward_points']
        
    # def get_user(self,request):
    #     return self.booking.user
    
    # def get_reward_points(self,request):
    #     if self.booking.is_match_ended == "True":
    #         reward_points = reward_points + 10/100 * (self.booking.price)
    #         return reward_points