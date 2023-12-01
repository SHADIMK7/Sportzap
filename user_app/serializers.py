from rest_framework import serializers
from . models import *
from owner_app . models import *

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['username', 'email', 'password', 'customer_mobile', 'customer_latitude', 'customer_longitude']
    
    def create(self, validated_data):
        account = Customer(
            username = validated_data['username'],
            email = validated_data['email'],
            customer_mobile = validated_data['customer_mobile']
        )
        account.set_password(validated_data['password'])
        account.save()
        return account
    
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
        
    def update(self, instance, validated_data):
        instance.team_name = validated_data.get('team_name', instance.team_name)
        instance.team_pic = validated_data.get('team_pic', instance.team_pic)
        instance.team_strength = validated_data.get('team_strength', instance.team_strength)
        instance.team_longitude = validated_data.get('team_longitude', instance.team_longitude)
        instance.team_latitude = validated_data.get('team_latitude', instance.team_latitude)
        instance.save()
        return instance
        
class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'
        
class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Team
        fields = '__all__'
        