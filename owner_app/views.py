from django.shortcuts import get_object_or_404
from .serializers  import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from user_app.models import *
# Create your views here.


class Registration(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    
    def post(self,request):
        data = {}
        phone_no = request.data.get('phone_no')
        if Owner.objects.filter(phone_no = phone_no).first():
            return Response({'status': "failed",'message': "Phone number already exists",'response_code':status.HTTP_400_BAD_REQUEST})
        
        email = request.data.get('email')
        if Owner.objects.filter(email=email).first():
            return Response({'status': "failed",'message': "Email already exists",'response_code':status.HTTP_400_BAD_REQUEST})
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            token, create = Token.objects.get_or_create(user=account)
            token_key = token.key
            print('token ', token)
            data ={
                "message":"Account Created Successfully",
                "Organization_name":account.Organization_name,
                "username":account.username,
                "email":account.email,
                "Phone number":account.phone_no,
                "token":token_key
            }   
        else:
            data = serializer.errors
        
        return Response(data)
    
    
    
class TurfCreate(generics.CreateAPIView, generics.ListAPIView):
    queryset = Turf.objects.all()
    serializer_class = TurfSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            d = serializer.save()
            data = {
                "message" : "turf created successfully",
                "turf name" : d.name
            }
            return Response(data)
        else:
            return Response(serializer.errors)
        
class TurfManagement(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TurfSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Turf.objects.filter(pk=pk)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object() 
        self.perform_destroy(instance)
        return Response({'status':"Destroyed",'message': "Turf has been deleted successfully",'response_code': status.HTTP_204_NO_CONTENT,})    
    
    
    
# class PaymentHistory(generics.ListCreateAPIView):
#     queryset = PaymentHistory.objects.all()
#     serializer_class = PaymentHistorySerializer

# class PaymentHistoryDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = PaymentHistory.objects.all()
#     serializer_class = PaymentHistorySerializer

class UpdatePaymentHistoryView(generics.UpdateAPIView):
    def put(self, request, booking_id, *args, **kwargs):
        booking = get_object_or_404(TurfBooking, pk=booking_id)
        
        if booking.has_expired():
            PaymentHistory.objects.create(user=booking.user, amount=booking.price)
            return Response({'message': 'Payment added to history.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Booking has not expired yet.'}, status=status.HTTP_400_BAD_REQUEST)