from rest_framework import serializers
from . models import *


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['Organization_name', 'username', 'email', 'password', 'Phone_number']

    def save(self):
        account = Owner(
            Organization_name=self.validated_data['Organization_name'],
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            Phone_number=self.validated_data['Phone_number'],
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