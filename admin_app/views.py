from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,generics,mixins
from owner_app.models import *
from django.http import Http404
from datetime import datetime, timedelta
from django.db.models import Sum
from decimal import Decimal
from django.db.models import F, Sum,Count
from admin_app.serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from admin_app.models import Leaderboard

class OwnerList(generics.ListAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
        
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})


    
class OwnerRetrieveDelete(generics.RetrieveDestroyAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    def get(self,request,pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})

    def delete(self, request,pk):
        instance = self.get_object() 
        # self.perform_destroy(instance)
        instance.delete()
        return Response({"status": "success", "message": "Deleted successfully", "response_code": status.HTTP_200_OK})


class TurfList(generics.ListAPIView):
    queryset = Turf.objects.all()
    serializer_class = TurfSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})

   

class TurfActiveDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Turf.objects.all()
    serializer_class = TurfSerializer
    def get(self,request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})

    def delete(self, request, pk):
        instance = self.get_object() 
        instance.delete()
        return Response({"status": "success", "message": "Deleted successfully", "response_code": status.HTTP_200_OK})
     
    def patch(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
      
class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})


class CustomerListDelete(generics.RetrieveDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer
    def get(self,request,pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"status": "success", "message": "User deleted Successfully", "response_code": status.HTTP_200_OK})


class TurfBookingView(generics.ListAPIView):
    queryset = TurfBooking.objects.all()
    serializer_class = BookingSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})
    
class TurfBookingCancel(generics.RetrieveDestroyAPIView):
    queryset = TurfBooking.objects.all()
    serializer_class = BookingSerializer

    def get(self,request,pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})

    def delete(self, request,pk):
        instance = self.get_object()
        instance.delete()
        return Response( {"status": "success", "message": "Turf booking cancelled", "response_code" :status.HTTP_200_OK})


class TransactionHistory(generics.ListAPIView):
    queryset = PaymentHistoryModel.objects.all()
    serializer_class = TransactionHistorySerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})
      


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

        data = {
            'monthly_income': monthly_income,
            'total_income': yearly_income,
            'monthly_balance_amount':monthly_balance_amount,
            'yearly_balance_amount':yearly_balance_amount
        }
        
        return Response({"status": "success", "message": data, "response_code": status.HTTP_200_OK})



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


# from django.db.models import F, Sum, Count, Case, When, DecimalField, Value

# class AdminView(APIView):
#     def get(self, request):
#         turf_credits = (
#             TurfBooking.objects.values('turf__name', 'turf__price')
#             .annotate(
#                 amount_credited_to_admin=Sum(
#                     Case(
#                         When(Payment_type='Partial_payment', then=F('price') * 0.20),
#                         default=F('price') * 0.80,
#                         output_field=DecimalField()
#                     )
#                 ),
#                 total_bookings=Count('turf')
#             )
#             .order_by('turf__name')
#         )

#         credited_amounts = []
#         for turf_credit in turf_credits:
#             remaining_amount = Decimal(turf_credit['turf__price']) - Decimal(turf_credit['amount_credited_to_admin'] or 0)
#             if remaining_amount > 0:
#                 amount_credited_to_admin = min(Decimal(turf_credit['turf__price']), remaining_amount)
#                 # amount_credited_to_turf = Decimal(turf_credit['turf__price']) - amount_credited_to_admin
#                 # amount_credited_to_turf = Decimal(turf_credit['turf__amount_paid']) - amount_credited_to_admin
#             else:
#                 amount_credited_to_admin = Decimal(turf_credit['turf__price'])
#                 amount_credited_to_turf = 0

#             credited_amounts.append({
#                 'turf_name': turf_credit['turf__name'],
#                 'turf_price': turf_credit['turf__price'],
#                 'amount_credited_to_admin': amount_credited_to_admin,
#                 'total_bookings': turf_credit['total_bookings'],
#                 'amount_credited_to_turf': amount_credited_to_turf
#             })

#         serializer = AdminIncomeSerializer({'bookings': credited_amounts})
#         return Response(serializer.data)

# from rest_framework.authtoken.models import Token

# class LogoutView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             # Retrieve the user's token
#             token = Token.objects.get(user=request.user)
#             # Delete the token
#             token.delete()
#             return Response({"status": "success", "message": "Logout successful", "response_code": status.HTTP_200_OK})
#         except Token.DoesNotExist:
#             return Response({"status": "failed", "message": "No token found", "response_code": status.HTTP_404_NOT_FOUND})


class LeaderBoard(generics.ListAPIView):
    serializer_class = LeaderBoardSerializer

    def get_queryset(self):
        queryset = Leaderboard.objects.order_by('-win_ratio','-aggregate_score_ratio')
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})


class PlayerLeaderBoard(generics.ListAPIView):
    serializer_class = PlayerLeaderBoardSerializer

    def get_queryset(self):
        queryset = Player.objects.annotate(no_of_win=Count('team__leaderboard__number_of_wins')).order_by('-no_of_win')
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})



class AmenityView(generics.ListCreateAPIView):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "message":serializer.data, "response_code":status.HTTP_201_CREATED})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
    def list(self,request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})


class AmenityDelete(generics.RetrieveDestroyAPIView):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    def get(self,request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})

    def delete(self, request, pk):
        instance = self.get_object() 
        instance.delete()
        return Response({"status": "success", "message": "Deleted successfully", "response_code": status.HTTP_200_OK})
     
    

class RewardView(generics.ListCreateAPIView):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "message":serializer.data, "response_code":status.HTTP_201_CREATED})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)          
      
    def list(self,request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})


class RewardUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    def get(self,request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})

    def delete(self, request, pk):
        instance = self.get_object() 
        instance.delete()
        return Response({"status": "success", "message": "Deleted successfully", "response_code": status.HTTP_200_OK})
     
    def patch(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    