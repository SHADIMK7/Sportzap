from rest_framework import serializers
from . models import *


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['Organization_name', 'username', 'email', 'password', 'phone_no']
        extra_kwargs = {
            'email': {'required': True, 'validators': []},
        }

    def save(self):
        account = Owner(
            Organization_name=self.validated_data['Organization_name'],
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            phone_no=self.validated_data['phone_no'],
        )
        account.set_password(self.validated_data['password'])
        account.save()
        return account


class TurfSerializer(serializers.ModelSerializer):
    amenity = serializers.PrimaryKeyRelatedField(queryset = Amenity.objects.all(), many=True)
    
    class Meta:
        model = Turf
        fields = "__all__"
        
    def create(self, validate_data):
        turf = Turf(
            name = validate_data['name'].capitalize(),
            location = validate_data['location'],
            image = validate_data['image'],
            price = validate_data['price'],
            description = validate_data['description'],
            amenity = validate_data['amenity']
        )
        turf.save()
        return turf
    
    


class PaymentHistorySerializer(serializers.ModelSerializer):
    turf = serializers.SerializerMethodField()
    price = serializers.FloatField(source='turf_booking.price')
    user_name = serializers.CharField(source='turf_booking.user_name')
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField() 
    amount_paid = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()
    class Meta:
        model = PaymentHistoryModel
        fields = ['turf','turf_booking', 'price', 'user_name','start_time','end_time','amount_paid', 'balance']
        
    def get_turf(self, object):
        return object.turf.id if object.turf else None
        
    def get_start_time(self,object):
        return object.turf_booking.start_time
    
    def get_end_time(self,object):
        return object.turf_booking.end_time
    
    def get_amount_paid(self,object):
        return object.turf_booking.amount_paid
    
    def get_balance(self,object):
        return object.turf_booking.balance


class MatchRatingSerializer(serializers.ModelSerializer):
    team1 = serializers.SerializerMethodField()
    team1_score = serializers.SerializerMethodField()
    team2 = serializers.SerializerMethodField()
    team2_score = serializers.SerializerMethodField()
    date_played = serializers.SerializerMethodField()
    model = MatchRatingModel
    fields = ['match', 'turf', 'remark', 'team1', 'team2', 'team1_score', 'team2_score', 'date_played'] 
    
    def get_team1(self, object):
        return object.match.team1
    
    def get_team2(self, object):
        return object.match.team2
    
    def get_team1_score(self,object):
        return object.match.team1
    
    def get_team2_score(self,object):
        return object.match.team2
    
    def get_date_played(self,object):
        return object.match.date_played