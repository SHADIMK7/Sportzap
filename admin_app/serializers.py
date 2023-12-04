from rest_framework import serializers
from owner_app.models import *
from user_app.models import *
from django.contrib.auth import get_user_model



class CustomerListSerializer(serializers.ModelSerializer):
    booking_count = serializers.SerializerMethodField()
    
    class Meta:
        model= Customer
        fields=['id','username', 'email', 'password', 'customer_mobile','booking_count']

    def get_booking_count(self, customer):
        booking_count = TurfBooking.objects.filter(user=customer).count()
        return booking_count
    


class TurfSerializer(serializers.ModelSerializer):
    amenity = serializers.PrimaryKeyRelatedField(queryset = Amenity.objects.all(), many=True)

    class Meta:
        model = Turf
        fields = '__all__'



class AbstractUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Abstract
        fields = ['first_name','last_name','email','phone_no']

class OwnerSerializer(serializers.ModelSerializer):

    abstract_user_details = AbstractUserSerializer(source='abstract', read_only=True)
    turf = serializers.SerializerMethodField()

    class Meta:
        model = Owner
        fields = ['id', 'abstract_user_details', 'turf']

    def get_turf(self, owner):
        turfs = owner.turf_set.all()
        turf_serializer = TurfSerializer(turfs, many=True)
        return turf_serializer.data
    
# class OwnerSerializer(serializers.ModelSerializer):
#     turf = serializers.SerializerMethodField()

#     class Meta:
#         model = Owner
#         fields = ['id', 'user_name',  'turf']
#     def get_turf(self, owner):
#         turfs = owner.turf_set.all()
#         turf_serializer = TurfSerializer(turfs, many=True)
#         return turf_serializer.data

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


class IncomeSerializer(serializers.Serializer):

    monthly_income = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_income = serializers.DecimalField(max_digits=10, decimal_places=2)
    monthly_balance_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    yearly_balance_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
   

# class AdminIncomeSerializer(serializers.Serializer):
#     amount_credited = serializers.DecimalField(max_digits=10, decimal_places=2)

class AdminIncomeSerializer(serializers.Serializer):
    bookings = serializers.ListField(child=serializers.DictField())


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
    