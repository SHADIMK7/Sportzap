from rest_framework import serializers
from . models import *


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['Organization_name', 'first_name', 'last_name', 'email', 'password', 'Phone_number']

    def save(self):
        account = Owner(
            Organization_name=self.validated_data['Organization_name'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            Phone_number=self.validated_data['Phone_number'],
        )
        account.set_password(self.validated_data['password'])
        account.save()
        return account


class TurfSerializer(serializers.ModelSerializer):
    turf_amenity = serializers.PrimaryKeyRelatedField(queryset = Amenity.objects.all(), many=True)
    
    class Meta:
        model = Turf
        fields = '_all_'
        
    def create(self, validate_data):
        turf = Turf(
            turf_name = validate_data['turf_name'].capitalize(),
            turf_location = validate_data['turf_location'],
            turf_image = validate_data['turf_image'],
            turf_price = validate_data['turf_price'],
            turf_description = validate_data['turf_description'],
            turf_amenity = validate_data['turf_amenity']
        )
        turf.save()
        return turf