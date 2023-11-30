from django.shortcuts import render
from rest_framework.response import Response
from owner_app.models import Owner,Turf
from owner_app.serializers import RegistrationSerializer,TurfSerializer
from rest_framework.views import APIView
from rest_framework import status
from admin_app.serializers import IncomeSerializer
from rest_framework import generics,mixins
from user_app.serializers import RegisterUserSerializer
from user_app.models import Customer
from admin_app.serializers import TurfUpdateSerializer,CustomerListSerializer
from django.http import Http404
from datetime import datetime, timedelta
from django.db.models import Sum
from owner_app.models import TurfBooking


# Create your views here.
class OwnerList(APIView):
    def get(self,request):
        owner= Owner.objects.filter(is_staff=False)
        serializer= RegistrationSerializer(owner,many=True,context={'request': request})
        return Response(serializer.data)
    
    
class OwnerDelete(APIView):
    def delete(self,request,username):
        try:
            stream=Owner.objects.get(username=username)
            stream.delete()
            return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Owner.DoesNotExist:
            return Response({"message": "Object does not exist"}, status=status.HTTP_404_NOT_FOUND)
        

class TurfList(generics.ListAPIView):
    queryset = Turf.objects.all()
    serializer_class = TurfSerializer

   

class TurfActiveDelete(APIView):
    queryset = Turf.objects.all()
    serializer_class = TurfSerializer
    lookup_field = 'id'
    def get_object(self):
        try:
            return self.queryset.get(pk=self.kwargs[self.lookup_field])
        except Turf.DoesNotExist:
            raise Http404
    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Turf.DoesNotExist:
            return Response({"message": "Object does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = True  
        instance.save()
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer
    
# class TurfBookingView(APIView):
#     def get(self,request):
#         booking= TurfBooking.objects.all()
#         serializer= BookingSerializer(booking,many=True)
#         return Response(serializer.data)
    

# class AdminDataView(APIView):
#     def get(self, request):
#             reversed_court = TurfBooking.objects.all().order_by('-id')
#             current_date = datetime.now()
            
#             first_day = current_date.replace(day=1)
#             last_day = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
#             income = TurfBooking.objects.filter(
#                 date__range=[first_day, last_day], payment_status='SUCCESS'
#             ).aggregate(total=Sum('price'))['total'] or 0
            
#             year_first_day = current_date.replace(month=1, day=1)
#             year_last_day = current_date.replace(month=12, day=31)
            
#             yearly_income = TurfBooking.objects.filter(
#                 date__range=[year_first_day, year_last_day], payment_status='SUCCESS'
#             ).aggregate(total=Sum('price'))['total'] or 0 
            
#             reversed_court_status = TurfBooking.objects.filter(payment_status='SUCCESS').order_by('-id')
            
#             data = {
#                 'income': income,
#                 'court': reversed_court,
#                 'yearly_income': yearly_income,
#                 'court_status': reversed_court_status.values()  # Convert to list of dicts
#             }
            
#             return Response(data)
        
 