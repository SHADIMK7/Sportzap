from django.shortcuts import get_object_or_404
from .serializers  import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from user_app.models import *
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate

# Create your views here.



class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Both username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Use the custom authentication backend
        user = authenticate(request, username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            user_type = user.usertype

            response_data = {
                'token': token.key,
                'user_type': user_type,
                'is_admin': user.is_superuser,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class Registration(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        data = {}
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            token, create = Token.objects.get_or_create(user=account.abstract)
            token_key = token.key
            data = {
                "message": "Account Created Successfully",
                "Organization_name": account.Organization_name,
                "username": account.abstract.username,
                "email": account.abstract.email,
                "Phone number": account.abstract.phone_no,
                "token": token_key
            }
            return Response({'status':"success",'message': data,'response_code': status.HTTP_201_CREATED,})
        else:
            data = serializer.errors

        return Response(data)
    
    
    
class TurfCreate(generics.CreateAPIView, generics.ListAPIView):
    # queryset = Turf.objects.all()
    serializer_class = TurfSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Turf.objects.filter(owner__pk=pk)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        serializer = self.serializer_class(data=request.data, context={'owner_pk': pk})
        if serializer.is_valid():
            d = serializer.save()
            data = {
                "message": "turf created successfully",
                "owner" : d.owner.pk,
                "turf name": d.name,
                "location" : d.location,
                "price" : d.price,
                # "image" : d.image,
                "description" : d.description,
                # "amenity" : d.amenity.name,
                "latitude" : d.latitude,
                "longitude" : d.longitude
            }
            return Response({'status':"success",'message': data,'response_code': status.HTTP_201_CREATED,})
        else:
            return Response(serializer.errors)
        
class TurfManagement(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TurfSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Turf.objects.filter(pk=pk)
    
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        updated_data = {
            'owner': instance.owner,
            'name': serializer.validated_data.get('name', instance.name),
            'location': serializer.validated_data.get('location', instance.location),
            'price': serializer.validated_data.get('price', instance.price),
            'image': serializer.validated_data.get('image', instance.image),
            'description': serializer.validated_data.get('description', instance.description),
            'amenity': [amenity.name for amenity in serializer.validated_data.get('amenity', instance.amenity.all())],
            'latitude': serializer.validated_data.get('latitude', instance.latitude),
            'longitude': serializer.validated_data.get('longitude', instance.longitude),
        }

        return Response({
            'status': "success",
            'message': "Turf updated successfully",
            'data': updated_data,
            'response_code': status.HTTP_200_OK,
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object() 
        self.perform_destroy(instance)
        return Response({'status':"success",'message': "Turf deleted successfully",'response_code': status.HTTP_200_OK,})


    
class PaymentHistory(generics.ListAPIView):
    # queryset = PaymentHistoryModel.objects.all()
    serializer_class = PaymentHistorySerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return PaymentHistoryModel.objects.filter(turf__pk=pk)
    
    # def get(self,request,*args, **kwargs):
    #     PaymentHistoryModel.objects.filter(turf__pk=kwargs['pk'])
    #     return Response({"success"})
        
    # def post(self, request, *args, **kwargs):
    #     return super().post(request, *args, **kwargs)   
        

class MatchRating(generics.ListCreateAPIView):
    serializer_class = MatchRatingSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return MatchRatingModel.objects.filter(turf_booking__pk=pk)   
    
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        serializer = self.serializer_class(data=request.data, context={'owner_pk': pk})
        
        if serializer.is_valid():
            content = serializer.save()
            
            response_data = {
                'status': "success",
                'message': "Match has been rated successfully",
                'response_code': status.HTTP_201_CREATED,
                'data': serializer.data,
            }
            
            return Response(response_data)
        else:
            return Response(serializer.errors)

    
    
# class PaymentHistory(generics.ListCreateAPIView):
#     queryset = PaymentHistory.objects.all()
#     serializer_class = PaymentHistorySerializer

# class PaymentHistoryDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = PaymentHistory.objects.all()
#     serializer_class = PaymentHistorySerializer

# class UpdatePaymentHistoryView(generics.UpdateAPIView):
#     def put(self, request, booking_id, *args, **kwargs):
#         booking = get_object_or_404(TurfBooking, pk=booking_id)
        
#         if booking.has_expired():
#             PaymentHistory.objects.create(user=booking.user, amount=booking.price)
#             return Response({'message': 'Payment added to history.'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'message': 'Booking has not expired yet.'}, status=status.HTTP_400_BAD_REQUEST)