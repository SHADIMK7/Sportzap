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
        user_latitude = float(self.request.query_params.get('latitude', 0))
        user_longitude = float(self.request.query_params.get('longitude', 0))

        user_location = (user_latitude, user_longitude)

        turfs = Turf.objects.all()
        turfs_with_distance = sorted(
            turfs,
            key=lambda turf: distance(user_location, (turf.latitude, turf.longitude)).miles
        )
        return turfs_with_distance
    
class TeamView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    
class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    # lookup_field = "id"
    
    def get(self, request, name):
        self.queryset = self.queryset.filter(id = name).first()
        if self.queryset:
            serializer = self.get_serializer(self.queryset)
            return Response({'data': serializer.data})
        else:
            return Response({'error': 'not found'}, status=status.HTTP_403_FORBIDDEN)
        
    def put(self, request, name):
        self.queryset = self.queryset.filter(id = name).first()
        serializer = self.get_serializer(self.queryset, data = request.data)
        print('HI')
        if serializer.is_valid():
            print('HI ENTERED')
            serializer.save()
            return Response({'status': "success",
                             'message': "updated successfully",
                             'response_code': status.HTTP_200_OK,
                             'data': serializer.data})
        else:
            return Response({'error': 'not updated'},
                            status=status.HTTP_403_FORBIDDEN)
            
    def patch(self, request, name):
        self.queryset = self.queryset.filter(id = name).first()
        serializer = self.get_serializer(self.queryset, data = request.data, partial=True)
        print('HI')
        if serializer.is_valid():
            print('HI ENTERED')
            serializer.save()
            return Response({'status': "success",
                             'message': "updated successfully",
                             'response_code': status.HTTP_200_OK,
                             'data': serializer.data})
        else:
            return Response({'error': 'not updated'},
                            status=status.HTTP_403_FORBIDDEN)
        
    def delete(self, request, name):
        self.queryset = self.queryset.filter(id = name).first()
        self.perform_destroy(self.queryset)
        return Response({'status': "success", 'message': "deleted successfully", 'response_code': status.HTTP_204_NO_CONTENT})
    
class PlayerView(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    
class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    lookup_field = "name"
    
#     def get(self, request, name):
#         self.queryset = self.queryset.filter(player_name = name).first()
#         if self.queryset:
#             serializer = self.get_serializer(self.queryset)
#             return Response({'data': serializer.data})
#         else:
#             return Response({'error': 'not found'}, status=status.HTTP_403_FORBIDDEN)
        
#     def put(self, request, name):
#         self.queryset = self.queryset.filter(player_name = name).first()
#         serializer = self.get_serializer(self.queryset, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'status': "success", 'message': "updated successfully", 'response_code': status.HTTP_200_OK, 'data': serializer.data})
#         else:
#             return Response({'error': 'not updated'}, status=status.HTTP_403_FORBIDDEN)
            
        
#     def delete(self,request,name):
#         self.queryset = self.queryset.filter(player_name = name).first()
#         self.perform_destroy(self.queryset)
#         return Response({'status': "success", 'message': "deleted successfully", 'response_code': status.HTTP_204_NO_CONTENT})