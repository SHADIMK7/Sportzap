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
from admin_app.models import Leaderboard
from rest_framework.permissions import IsAdminUser


class OwnerList(generics.ListAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]

    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
        
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "response_code": status.HTTP_200_OK, "message": serializer.data})


    
class OwnerRetrieveDelete(generics.RetrieveDestroyAPIView):

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]

    queryset = Owner.objects.all()
    serializer_class = OwnerTurfSerializer

    def get(self,request,pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})

    def delete(self, request,pk):
        instance = self.get_object() 
        instance.delete()
        return Response({"status": "success", "message": "Deleted successfully", "response_code": status.HTTP_200_OK})


class TurfList(generics.ListAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]

    queryset = Turf.objects.all()
    serializer_class = TurfSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})

   

class TurfActiveDelete(generics.RetrieveUpdateDestroyAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]

    queryset = Turf.objects.all()
    serializer_class = TurfUpdateSerializer

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
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]

    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})


class CustomerListDelete(generics.RetrieveDestroyAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]

    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer
    def get(self,request,pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})

    def delete(self, request, pk):
        instance = self.get_object()
        instance.delete()
        # self.perform_destroy(instance)
        return Response({"status": "success", "message": "User deleted Successfully", "response_code": status.HTTP_200_OK})


class TurfBookingView(generics.ListAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]

    queryset = TurfBooking.objects.all()
    serializer_class = BookingSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})
    
class TurfBookingCancel(generics.RetrieveDestroyAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]

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
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]

    queryset = PaymentHistoryModel.objects.all()
    serializer_class = TransactionHistorySerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})
      


class AdminIncomeView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]

    def post(self, request):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return Response(
                {"status": "error", "message": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        total_income = self.calculate_income(start_date, end_date)

        data = {
            'total_income': total_income,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d')
        }
        
        return Response({"status": "success", "message": data, "response_code": status.HTTP_200_OK})

    def calculate_income(self, start_date, end_date):
        total_income = TurfBooking.objects.filter(
            date__range=[start_date, end_date]
        ).aggregate(total=Sum('amount_paid'))['total'] or 0

        return total_income
    
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




    


#   ///// AI

from collections import defaultdict

class TurfWeeklyIncomeView(APIView):
    def get(self, request):
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # turf_income = defaultdict(list)
        response_data = []

        for i in range(52):  
            start_date = start_of_week - timedelta(weeks=i)
            end_date = end_of_week - timedelta(weeks=i)
            income = TurfBooking.objects.filter(
                date__range=[start_date, end_date]
            ).values('turf__id', 'turf__name').annotate(total_income=Sum('price')).annotate(total_booking=Count('id'))

            for data in income:
                turf_id = data['turf__id']
                turf_name = data['turf__name']
                total_income = data['total_income']
                total_booking = data['total_booking']

                response_data.append({
                    'start_date': start_date.strftime('%Y-%m-%d'),
                    'end_date': end_date.strftime('%Y-%m-%d'),
                    'turf_id': turf_id,
                    'turf_name': turf_name,
                    'income': total_income,
                    'booking': total_booking 
                })

        return Response(response_data)


#   //////////////////    AI 
# 
# 
#  
# from collections import defaultdict
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta 

class TurfMonthlyIncomeView(APIView):
    def get(self, request):
        today = datetime.now()
        start_of_month = today.replace(day=1)

        # end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        start_of_previous_month = start_of_month - relativedelta(months=1)
        end_of_previous_month = start_of_month - timedelta(days=1)
        
        # turf_income = defaultdict(list)

        # for i in range(12):
        #     start_date = start_of_month - relativedelta(months=i)

        #     end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        response_data = []

        income = TurfBooking.objects.filter(
                date__range=[start_of_previous_month, end_of_previous_month]
            ).values('turf__id', 'turf__name','turf__price','turf__owner').annotate(total_income=Sum('price')).annotate(total_booking=Count('id'))

        for data in income:
                turf_id = data['turf__id']
                turf_owner = data['turf__owner']
                turf_name = data['turf__name']
                total_income = data['total_income']
                total_booking = data['total_booking']
                price = data['turf__price']
                response_data.append({
                    'turf_id':turf_id,
                    'turf_owner' : turf_owner ,
                    'start_date': start_of_previous_month.strftime('%Y-%m-%d'),
                    'end_date': end_of_previous_month .strftime('%Y-%m-%d'),
                    'month':start_of_previous_month.strftime("%B"),
                    'turf_name': turf_name,
                    'income': total_income,
                    'booking': total_booking,
                    'price': price
                })

        return Response(response_data)


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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

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
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

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
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]

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
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]

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
    

from geopy.distance import distance 
from django.shortcuts import get_object_or_404

class TurfDisplayView(generics.RetrieveAPIView):
    serializer_class = TurfSerializer

    def get_queryset(self):
        pk = self.kwargs.get('id')  
        user = Customer.objects.get(pk=pk)

        customer_latitude = float(user.customer.latitude)
        customer_longitude = float(user.customer.longitude)
        # customer_latitude = 11.0732 
        # customer_longitude = 76.0740  
        customer_location = (customer_latitude, customer_longitude)
        
        all_turfs = Turf.objects.all() 
        
        turf_distances = {
            turf: distance(customer_location, (turf.latitude, turf.longitude)).km
            for turf in all_turfs
        }
        print(turf_distances)
        # turf_lati = 51.5074  # Latitude for London
        # turf_longi = -0.1278  # Longitude for London
        # Sort Turf instances by distance
        sorted_turfs = sorted(turf_distances, key=turf_distances.get)
        # dist = distance(customer_location, (turf_lati, turf_longi)).miles
        print(sorted_turfs)
        return sorted_turfs
    
    def get(self,request,id):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})


# //////   AI

from django.db.models import Count, Sum

class TurfDateBookingView(generics.ListAPIView):
    serializer_class = BookingDateSerializer

    def get_queryset(self):
        queryset  = (
            TurfBooking.objects
            .values('date', 'turf')
            .annotate(total_bookings=Count('id')).annotate(total_earnings=Sum('price'))
            .order_by('date', 'turf')
        )
        return queryset
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success" , "response_code": status.HTTP_200_OK, "message": serializer.data})
   


class CustomerLocationView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerLocationSerializer

    def get_object(self):
        try:
            customer = Customer.objects.get(pk = self.kwargs.get('id')  )
            return customer.customer  
        except Customer.DoesNotExist:
            raise Http404("Customer does not exist")
    # def get_object(self):
    #     return self.request.user 

    def patch(self, request, id):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLocationFetch(APIView):
    def get(self, request):
        # latitude_str = self.request.query_params.get('latitude')
        # longitude_str = self.request.query_params.get('longitude')
        latitude_str = 40.7128
        longitude_str = 74.0060
        latitude = float(latitude_str)
        longitude = float(longitude_str)
        user_location = (latitude, longitude)
        
        all_turfs = Turf.objects.all() 
        turf_data = []
        for turf in all_turfs:
            amenities = [amenity.name for amenity in turf.amenity.all()]
            image_url = request.build_absolute_uri(turf.image.url)  # Construct absolute image URL

            turf_data.append({
                'id': turf.id,
                'name': turf.name, 
                'location': turf.location,
                'price': turf.price,
                'image': image_url,
                'description': turf.description,
                'amenities': amenities,
                'distance_km': distance(user_location, (turf.latitude, turf.longitude)).km
            })

        sorted_turfs = sorted(turf_data, key=lambda x: x['distance_km'])
        return Response({"status": "success", "response_code": status.HTTP_200_OK, "message": sorted_turfs})

class MatchRatingView(APIView):
    def get(self, request):
        match_ratings = MatchRatingModel.objects.values('id', 'team1_id','team2_id','team1_score','team2_score','date_played','players_data')

        response_data = []

        for data in match_ratings:
                match_id = data['id']
                team1_id = data['team1_id']
                team1_score = data['team1_score']
                team2_id = data['team2_id']
                team2_score = data['team2_score']
                date_played = data['date_played']
                players_data = data['players_data']
                if team1_score>team2_score:
                    team1_result = "win"
                    team2_result = "loss"
                else: 
                    team1_result = "loss"
                    team2_result = "win"
                team1_players = players_data.get('team1_player', [])
                team2_players = players_data.get('team2_player', [])
               
                response_data.append({
                    'match_id':match_id,
                    'team_id' : team1_id ,
                    'result': team1_result,
                    'date': date_played,
                    'players':team1_players
                })
                response_data.append({
                    'match_id':match_id,
                    'team_id' : team2_id ,
                    'result': team2_result,
                    'date': date_played,
                    'players':team2_players
                })
                
        return Response({"status": "success", "response_code": status.HTTP_200_OK, "message": response_data})


import requests
        
class DisplayWeeklyIncomeData(APIView):
    def get(self, request):
        ai_backend_url = 'https://a3fd-116-68-110-250.ngrok-free.app/income'

        try:
            response = requests.get(ai_backend_url)
            response.raise_for_status()  
            
            income_data = response.json()  

            return Response({"status": "success", "response_code": status.HTTP_200_OK, "message": income_data})
        
        except requests.RequestException as e:
            return Response({"status": "failure", "message": f"Request failed: {e}"})        

class DisplayWeeklyIncomeDataID(APIView):
    def get(self, request, turf_id):
        ai_backend_url = 'https://a3fd-116-68-110-250.ngrok-free.app/income'

        try:
            response = requests.get(ai_backend_url)
            response.raise_for_status()
            
            income_data = response.json()
            specific_turf_income = [income for income in income_data if income.get('turf_id') == turf_id]

            return Response({"status": "success", "specific_turf_income": specific_turf_income})
        
        except requests.RequestException as e:
            return Response({"status": "failure", "message": f"Request failed: {e}"})            
        