from rest_framework import serializers
from . models import *
from owner_app . models import *

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['username', 'email', 'password', 'customer_mobile']
    
    def create(self, validated_data):
        account = Customer(
            username = validated_data['username'],
            email = validated_data['email'],
            customer_mobile = validated_data['customer_mobile']
        )
        account.set_password(validated_data['password'])
        account.save()
        return account
    
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurfBooking
        fields = '__all__'