from rest_framework import serializers
from . models import *


# Update your RegistrationSerializer to use CustomUser
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
