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
    queryset = Turf.objects.all()
    serializer_class = TurfSerializer

    def post(self, request):
        # if request.user.usertype == 'owner':
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                d = serializer.save()
                data = {
                    "message": "turf created successfully",
                    "turf name": d.name
                }
                return Response({'status':"success",'message': data,'response_code': status.HTTP_201_CREATED,})
            else:
                return Response(serializer.errors)
        # else:
        #     return Response({'status': "failed",'message': "Only owners can create turfs",'response_code':status.HTTP_400_BAD_REQUEST})
        
class TurfManagement(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TurfSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Turf.objects.filter(pk=pk)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object() 
        self.perform_destroy(instance)
        return Response({'status':"success",'message': "Turf deleted successfully",'response_code': status.HTTP_200_OK,})


    
class PaymentHistory(generics.ListCreateAPIView):
    # queryset = PaymentHistoryModel.objects.all()
    serializer_class = PaymentHistorySerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return PaymentHistoryModel.objects.filter(turf__pk=pk)
    

class MatchRating(generics.ListCreateAPIView):
    # queryset = MatchRatingModel.objects.all()
    serializer_class = MatchRatingSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return MatchRatingModel.objects.filter(turf_booking__pk=pk)   
    
    def perform_create(self, serializer):
        print("entered")
        instance = serializer.save()
        serialized_data = MatchRatingSerializer(instance).data
        print("entered")
        response_data = {
            'status': "success",
            'message': "Match has been rated successfully",
            'response_code': status.HTTP_201_CREATED,
            'data': serialized_data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    
    
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