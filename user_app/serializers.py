from rest_framework import serializers
from . models import *
from owner_app . models import *

class AbstractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Abstract
        fields  = ['username', 'email', 'password' , 'phone_no', 'latitude', 'longitude']
        extra_kwargs = {
            'email': {'required': True},
        }
        
        def create(self, validated_data):
            validated_data = {
                'username': validated_data['username'],
                'email': validated_data['email'],
                'phone_no': validated_data['phone_no'], 
                'latitude': validated_data.get('latitude'),
                'longitude': validated_data.get('longitude'),
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
        
    # def update(self, instance, validated_data):
    #     instance.team_name = validated_data.get('team_name', instance.team_name)
    #     instance.team_pic = validated_data.get('team_pic', instance.team_pic)
    #     instance.team_strength = validated_data.get('team_strength', instance.team_strength)
    #     instance.team_longitude = validated_data.get('team_longitude', instance.team_longitude)
    #     instance.team_latitude = validated_data.get('team_latitude', instance.team_latitude)
    #     instance.save()
    #     return instance
        
class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'
        
class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Team
        fields = '__all__'