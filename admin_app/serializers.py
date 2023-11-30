from rest_framework import serializers
from owner_app.models import *
from user_app.models import *



class CustomerListSerializer(serializers.ModelSerializer):
    booking_count = serializers.SerializerMethodField()
    class Meta:
        model= Customer
        fields=['id','username', 'email', 'password', 'customer_mobile','booking_count']
    def get_booking_count(self, customer):
        booking_count = TurfBooking.objects.filter(user=customer).count()
        return booking_count
    
class RegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Owner
        fields= ['id','Organization_name', 'username', 'email', 'password', 'phone_no']

class TurfSerializer(serializers.ModelSerializer):
    amenity = serializers.PrimaryKeyRelatedField(queryset = Amenity.objects.all(), many=True)

    class Meta:
        model = Turf
        fields='__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurfBooking
        fields = '__all__'

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
    