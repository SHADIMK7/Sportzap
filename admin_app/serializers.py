from rest_framework import serializers
from owner_app.models import *
from user_app.models import *


class CustomerListSerializer(serializers.ModelSerializer):
    booking_count = serializers.SerializerMethodField()
    class Meta:
        model= Customer
        fields=['username', 'email', 'password', 'customer_mobile','booking_count']
    def get_booking_count(self, customer):
        bookings_count = TurfBooking.objects.filter(user=customer).count()
        return bookings_count
    


# class IncomeSerializer(serializers.Serializer):
#     monthly_income = serializers.DecimalField(max_digits=10, decimal_places=2)
#     total_income = serializers.DecimalField(max_digits=10, decimal_places=2)

    
class TurfUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only='True')
    name = serializers.CharField(read_only='True')
    location = serializers.CharField(read_only='True')
    price = serializers.BooleanField(read_only='True')
    image = serializers.ImageField(read_only='True')
    description = serializers.CharField(read_only='True')
    amenity = serializers.CharField(read_only='True')
    is_active = serializers.BooleanField(default=False)

#     def update(self,instance,validate_data):
#         instance.is_active=validate_data.get('is_active',instance.is_active)
#         instance.save()
#         return instance
    