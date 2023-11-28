from django.shortcuts import render
from rest_framework import generics, status
from . models import *
from . serializers import *
from rest_framework.response import Response

# Create your views here.
class CustomerRegistrationView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = RegisterUserSerializer
    
    def post(self, request): 
        mobile = request.data.get('customer_mobile')
        if Customer.objects.filter(customer_mobile = mobile).first():
            return Response({"detail":"Mobile already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        email = request.data.get('email')
        if Customer.objects.filter(email = email).first():
            return Response({"detail":"Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            data = {
                "message" : "Account created successfully",
                "username" : account.username
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)