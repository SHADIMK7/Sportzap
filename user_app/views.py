from django.shortcuts import render
from rest_framework import generics, status
from . models import *
from . serializers import *
from owner_app.models import *
from rest_framework.response import Response
from geopy.distance import distance

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
    serializer_class = TurfBookingSerializer
    

class TurfDisplayView(generics.ListAPIView):
    queryset = Turf.objects.all()
    serializer_class = TurfDisplaySerializer
    
    def get_queryset(self):
        # Get the user's location from the request, you may need to customize this based on your application
        user_latitude = float(self.request.query_params.get('latitude', 0))
        user_longitude = float(self.request.query_params.get('longitude', 0))

        user_location = (user_latitude, user_longitude)

        # Calculate distances and order by them
        turfs = Turf.objects.all()
        turfs_with_distance = sorted(
            turfs,
            key=lambda turf: distance(user_location, (turf.latitude, turf.longitude)).miles
        )
        return turfs_with_distance
    
class TeamView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

