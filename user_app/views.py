from django.shortcuts import render
from rest_framework import generics, status
from . models import *
from . serializers import *
from owner_app.models import *
from rest_framework.response import Response

# Create your views here.
class CustomerRegistrationView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = RegisterUserSerializer
    
    def post(self, request): 
        mobile = request.data.get('customer_mobile')
        if Customer.objects.filter(customer_mobile = mobile).first():
            return Response({'status': "failed",'message': "Mobile number already exists",'response_code':status.HTTP_400_BAD_REQUEST})
        
        email = request.data.get('email')
        if Customer.objects.filter(email = email).first():
            return Response({'status': "failed",'message': "Email already exists",'response_code':status.HTTP_400_BAD_REQUEST})
        
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
        
class BookingView(generics.ListCreateAPIView):
    queryset = TurfBooking.objects.all()
    serializer_class = BookingSerializer
    