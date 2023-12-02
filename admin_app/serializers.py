from rest_framework import serializers
from owner_app.models import *
from user_app.models import *
# from admin_app.serializers import TurfSerializer


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
        fields='__all__'


class OwnerSerializer(serializers.ModelSerializer):
    turf = serializers.SerializerMethodField()

    class Meta:
        model = Owner
        fields= ['id','Organization_name', 'username', 'email', 'password', 'phone_no','turf']
    def get_turf(self, owner):
        turfs = owner.turf_set.all()
        turf_serializer = TurfSerializer(turfs, many=True)
        return turf_serializer.data

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurfBooking
        fields = '__all__'

class TransactionHistorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(source='user.first_name')
    turf = serializers.StringRelatedField(source='turf.name')
    price = serializers.StringRelatedField(source="turf_booking.price")
    amount_paid = serializers.StringRelatedField(source="turf_booking.amount_paid" )
    balance = serializers.StringRelatedField(source = "turf_booking.balance")
    class Meta:
        model = PaymentHistoryModel
        fields = ['id', 'turf_booking', 'turf', 'user','amount_paid','price','balance'] 


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
    