from rest_framework import serializers
from . models import *
from rest_framework import status


class AbstractSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Abstract
        fields  = ['username', 'email', 'password' , 'phone_no', 'latitude', 'longitude', 'usertype']
        extra_kwargs = {
            'email': {'required': True, 'validators': []},
            'phone_no': {'required': True, 'validators': []},
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
            raise serializers.ValidationError({'status': "failed",'message': "Please use customer registration for registering customer. This registration is exclusively for TURF OWNERS",'response_code':status.HTTP_400_BAD_REQUEST})
        return abstract_data
        
    def create(self, validated_data):
        abstract_data = validated_data.pop('abstract')
        password = abstract_data.get('password')
        abstract = AbstractSerializer(data=abstract_data)
        if abstract.is_valid():
            
            email = abstract_data.get('email')
            if Abstract.objects.filter(email=email).exists():
                raise serializers.ValidationError({'status': "failed",'message': "This email is already registered",'response_code':status.HTTP_400_BAD_REQUEST})
            
            phone_no = abstract_data.get('phone_no')
            if Abstract.objects.filter(phone_no=phone_no).exists():
                raise serializers.ValidationError({'status': "failed",'message': "This phone no is already registered",'response_code':status.HTTP_400_BAD_REQUEST})
            
            abstract = abstract.save()
            abstract.set_password(password)
            abstract.save()
            account = Owner.objects.create(abstract=abstract, **validated_data)
            return account
        else:
            raise serializers.ValidationError({"abstract": abstract.errors})


class TurfSerializer(serializers.ModelSerializer):
    amenity = serializers.PrimaryKeyRelatedField(queryset=Amenity.objects.all(), many=True)

    class Meta:
        model = Turf
        exclude = ["owner"]

    def create(self, validated_data):
        owner_pk = self.context.get('owner_pk')
        amenity_data = validated_data.pop('amenity')
        turf = Turf.objects.create(owner_id=owner_pk, **validated_data)
        turf.amenity.set(amenity_data)

        return turf
    
    
# class TurfPriceUpdateSerializer(serializers.ModelSerializer):
#     old_price = serializers.SerializerMethodField()
#     turf_id = serializers.SerializerMethodField()
#     owner_id = serializers.SerializerMethodField()

#     class Meta:
#         model = TurfPriceUpdateModel
#         fields = ['turf_id','owner_id' , 'old_price', 'new_price']

#     def get_turf_id(self, object):
#         print("objects is ", object)
#         return object
    
#     def get_owner_id(self,object):
#         return object.owner.id

#     def get_old_price(self, obj):
#         return obj.turf.price
        


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
        fields = ['turf', 'turf_booking', 'price', 'user_name', 'start_time', 'end_time', 'amount_paid', 'balance']

    def get_turf(self, object):
        return object.turf.id if object.turf else None

    def get_start_time(self, object):
        return object.turf_booking.start_time if object.turf_booking else None

    def get_end_time(self, object):
        return object.turf_booking.end_time if object.turf_booking else None

    def get_amount_paid(self, object):
        return object.turf_booking.amount_paid if object.turf_booking else None

    def get_balance(self, object):
        return object.turf_booking.balance if object.turf_booking else None


class MatchRatingSerializer(serializers.ModelSerializer):
    is_match_ended = serializers.SerializerMethodField()

    class Meta:
        model = MatchRatingModel
        fields = ['team1', 'team2', 'team1_score', 'team2_score', 'date_played','turf_booking', 'turf', 'remark', 'is_match_ended']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['is_match_ended']:
            responce = {
            'status': "success",
            'message': "Match has been rated successfully",
            'response_code': status.HTTP_201_CREATED,
            'data': data,
        }
            return responce
        else: 
            raise serializers.ValidationError({'status': "failed",'message': "Match has not ended.",'response_code':status.HTTP_400_BAD_REQUEST})

    def get_is_match_ended(self, instance):
        turf_booking = instance.turf_booking
        return turf_booking.is_match_ended()
    