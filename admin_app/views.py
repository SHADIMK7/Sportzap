from django.shortcuts import render
from rest_framework.response import Response
from owner_app.models import Owner,Turf
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics,mixins
from user_app.models import Customer
from admin_app.serializers import TransactionHistorySerializer,TurfUpdateSerializer,CustomerListSerializer,OwnerSerializer,TurfSerializer,BookingSerializer,IncomeSerializer,AdminIncomeSerializer
from django.http import Http404
from datetime import datetime, timedelta
from django.db.models import Sum
from owner_app.models import TurfBooking,PaymentHistoryModel
from decimal import Decimal
from django.db.models import F, Sum,Count


# Create your views here.
class OwnerList(APIView):
    def get(self,request):
        owner= Owner.objects.filter(is_staff=False)
        serializer= OwnerSerializer(owner,many=True,context={'request': request})
        return Response(serializer.data)
    
    
class OwnerDelete(APIView):
    def delete(self,request,pk):
        try:

            stream=Owner.objects.get(pk=pk)
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

    # def put(self,request,pk):
    #     stream=StreamField.objects.get(pk=pk)
    #     serializer=StreamFieldSerializer(stream,data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors)
        

class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer

class CustomerListDelete(generics.RetrieveDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer
    
      
class TurfBookingView(APIView):
    def get(self,request):
        booking= TurfBooking.objects.all()
        serializer= BookingSerializer(booking,many=True)
        return Response(serializer.data)

class TurfBookingCancel(mixins.RetrieveModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = TurfBooking.objects.all()
    serializer_class = BookingSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class TransactionHistory(mixins.ListModelMixin,generics.GenericAPIView):
    queryset = PaymentHistoryModel.objects.all()
    serializer_class = TransactionHistorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)



class AdminIncomeView(APIView):
    def get(self, request):
        # Calculate monthly income
        current_date = datetime.now()
        first_day = current_date.replace(day=1)
        last_day = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        monthly_income = TurfBooking.objects.filter(
            date__range=[first_day, last_day]).aggregate(total=Sum('amount_paid'))['total'] or 0
        monthly_balance_amount = TurfBooking.objects.filter(
            date__range=[first_day, last_day]).aggregate(total=Sum('balance'))['total'] or 0

        # Calculate yearly income
        year_first_day = current_date.replace(month=1, day=1)
        year_last_day = current_date.replace(month=12, day=31)
        yearly_income = TurfBooking.objects.filter(
            date__range=[year_first_day, year_last_day]).aggregate(total=Sum('amount_paid'))['total'] or 0
        yearly_balance_amount = TurfBooking.objects.filter(
            date__range=[year_first_day, year_last_day]).aggregate(total=Sum('balance'))['total'] or 0

        serializer = IncomeSerializer({
            'monthly_income': monthly_income,
            'total_income': yearly_income,
            'monthly_balance_amount':monthly_balance_amount,
            'yearly_balance_amount':yearly_balance_amount
        })
        return Response(serializer.data)


# class AdminView(APIView):
#     def get(self, request):
#         price = TurfBooking.objects.filter('price')
#         amount_credited = price*5 / 100
#         serializer = AdminIncomeSerializer({
#             'amount_credited': amount_credited
#         })
#         return Response(serializer.data)

# class AdminView(APIView):
#     def get(self, request):
#         turf_credits = (
#             TurfBooking.objects.values('turf__name', 'turf__price')
#             .annotate(total_credits=Sum(F('price') * 0.20), total_bookings=Count('turf'))
#             .order_by('turf__name').annotate(amount_credited_to_turf=Sum(F('price') * 0.80))
#             .order_by('turf__name').annotate(balance_amount_to_turf=Sum(F('balance')))
#         )
      
#         credited_amounts = []
#         for turf_credit in turf_credits:
#             credited_amounts.append( {
#                 'turf_name': turf_credit['turf__name'],
#                 'turf_price': turf_credit['turf__price'],
#                 'amount_credited': Decimal(turf_credit['total_credits'] or 0),
#                 'total_bookings':turf_credit['total_bookings'],
#                 'amount_credited_to_turf':Decimal(turf_credit['amount_credited_to_turf'] or 0),
#                 'balance_amount_to_turf':Decimal(turf_credit['balance_amount_to_turf'] or 0)
#             })

#         serializer = AdminIncomeSerializer({'bookings': credited_amounts})
#         return Response(serializer.data)


from django.db.models import F, Sum, Count, Case, When, DecimalField, Value

class AdminView(APIView):
    def get(self, request):
        turf_credits = (
            TurfBooking.objects.values('turf__name', 'turf__price')
            .annotate(
                amount_credited_to_admin=Sum(
                    Case(
                        When(Payment_type='Partial_payment', then=F('price') * 0.20),
                        default=F('price') * 0.80,
                        output_field=DecimalField()
                    )
                ),
                total_bookings=Count('turf')
            )
            .order_by('turf__name')
        )

        credited_amounts = []
        for turf_credit in turf_credits:
            remaining_amount = Decimal(turf_credit['turf__price']) - Decimal(turf_credit['amount_credited_to_admin'] or 0)
            if remaining_amount > 0:
                amount_credited_to_admin = min(Decimal(turf_credit['turf__price']), remaining_amount)
                amount_credited_to_turf = Decimal(turf_credit['turf__price']) - amount_credited_to_admin
            else:
                amount_credited_to_admin = Decimal(turf_credit['turf__price'])
                amount_credited_to_turf = 0

            credited_amounts.append({
                'turf_name': turf_credit['turf__name'],
                'turf_price': turf_credit['turf__price'],
                'amount_credited_to_admin': amount_credited_to_admin,
                'total_bookings': turf_credit['total_bookings'],
                'amount_credited_to_turf': amount_credited_to_turf
            })

        serializer = AdminIncomeSerializer({'bookings': credited_amounts})
        return Response(serializer.data)
