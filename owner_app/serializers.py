from rest_framework import serializers
from . models import *



class AbstractSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Abstract
        fields  = ['username', 'email', 'password' , 'phone_no', 'latitude', 'longitude', 'usertype']
        extra_kwargs = {
            'email': {'required': True, 'validators': []},
        }
        
        def create(self, validated_data):
            abstract = Abstract.objects.create(validated_data)
            abstract.set_password(validated_data['password'])
            abstract.save()
            return abstract

class RegistrationSerializer(serializers.ModelSerializer):
    abstract = AbstractSerializer()
        
    class Meta:
        model = Owner
        fields = ['abstract','Organization_name']
    
    def validate_abstract(self, abstract_data):
        usertype = abstract_data.get('usertype')
        if usertype != 'owner':
            raise serializers.ValidationError({'usertype': 'Please use customer registration for registering customer. This registration is exclusively for TURF OWNERS'})
        return abstract_data
        
    def create(self, validated_data):
        abstract_data = validated_data.pop('abstract')
        password = abstract_data.get('password')
        abstract = AbstractSerializer(data=abstract_data)
        if abstract.is_valid():
            
            email = abstract_data.get('email')
            if Abstract.objects.filter(email=email).exists():
                raise serializers.ValidationError({'abstract': {'email': 'This email is already registered.'}})
            
            phone_no = abstract_data.get('phone_no')
            if Abstract.objects.filter(phone_no=phone_no).exists():
                raise serializers.ValidationError({'abstract': {'email': 'This phone no is already registered. '}})
            
            abstract = abstract.save()
            abstract.set_password(password)
            abstract.save()
            account = Owner.objects.create(abstract=abstract, **validated_data)
            return account
        else:
            raise serializers.ValidationError({"abstract": abstract.errors})


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
            amenity = validate_data['amenity'],
            latitude = validate_data['latitude'],
            longitude = validate_data['longitude']
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
    is_match_ended = serializers.SerializerMethodField()

    class Meta:
        model = MatchRatingModel
        fields = ['team1', 'team2', 'team1_score', 'team2_score', 'date_played','turf_booking', 'turf', 'remark', 'is_match_ended']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['is_match_ended']:
            return data
        else: 
            raise serializers.ValidationError({"abstract": "Match has not ended"})

    def get_is_match_ended(self, instance):
        turf_booking = instance.turf_booking
        return turf_booking.is_match_ended()
    