from django.shortcuts import render
from rest_framework.response import Response
from owner_app.models import Owner,Turf
from owner_app.serializers import RegistrationSerializer,TurfSerializer
from rest_framework.views import APIView
from rest_framework import status
from admin_app.serializers import IncomeSerializer
from rest_framework import generics,mixins



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

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TurfDelete(mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Turf.objects.all()
    serializer_class = TurfSerializer

    def delete(self, request, *args, **kwargs):
       return self.destroy(request, *args, **kwargs)



# class AdminDataView(APIView):
#     def get(self, request):
#             reversed_court = Court_booking.objects.all().order_by('-id')
#             current_date = datetime.now()
            
#             first_day = current_date.replace(day=1)
#             last_day = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
#             income = Court_booking.objects.filter(
#                 date__range=[first_day, last_day], payment_status='SUCCESS'
#             ).aggregate(total=Sum('price'))['total'] or 0
            
#             year_first_day = current_date.replace(month=1, day=1)
#             year_last_day = current_date.replace(month=12, day=31)
            
#             yearly_income = Court_booking.objects.filter(
#                 date__range=[year_first_day, year_last_day], payment_status='SUCCESS'
#             ).aggregate(total=Sum('price'))['total'] or 0 
            
#             reversed_court_status = Court_booking.objects.filter(payment_status='SUCCESS').order_by('-id')
            
#             data = {
#                 'income': income,
#                 'court': reversed_court,
#                 'yearly_income': yearly_income,
#                 'court_status': reversed_court_status.values()  # Convert to list of dicts
#             }
            
#             return Response(data)
#         
 