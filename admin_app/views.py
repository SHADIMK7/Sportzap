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
from rest_framework.pagination import PageNumberPagination


class OwnerList(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
        
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "response_code": status.HTTP_200_OK, "message": serializer.data})


    
class OwnerRetrieveDelete(generics.RetrieveDestroyAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Owner.objects.all()
    serializer_class = OwnerTurfSerializer
    def get_instance(self, pk):
        try:
            return self.get_queryset().get(pk=pk)
        except Owner.DoesNotExist:
            return None

    def get(self,request,pk):
      
            instance = self.get_instance(pk)
            if instance is not None:

               serializer = self.get_serializer(instance)
               return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})
            else:
               return Response({"status": "error", "message": "Owner does not exist", "response_code": status.HTTP_404_NOT_FOUND})
    
    def delete(self, request,pk):
       

            instance = self.get_instance(pk)
            if instance is not None:
                instance.delete()
                return Response({"status": "success", "message": "Deleted successfully", "response_code": status.HTTP_200_OK})
            else:
               return Response({"status": "error", "message": "Owner does not exist", "response_code": status.HTTP_404_NOT_FOUND})
    


class CustomPagination(PageNumberPagination):
    page_size = 10 
    # page_size_query_param = 'page_size'


class TurfList(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]


    queryset = Turf.objects.all()
    serializer_class = TurfSerializer
    pagination_class = CustomPagination

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        # if page is not None:
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})

       
   

class TurfActiveDelete(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Turf.objects.all()
    serializer_class = TurfUpdateSerializer

    def get_instance(self, pk):
        try:
            return self.get_queryset().get(pk=pk)
        except Turf.DoesNotExist:
            return None

    def get(self,request, pk):
        instance = self.get_instance(pk)
        if instance is not None:

            serializer = self.get_serializer(instance)
            return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})
        else:
               return Response({"status": "error", "message": "Turf does not exist", "response_code": status.HTTP_404_NOT_FOUND})
    
    def delete(self, request, pk):
        instance = self.get_instance(pk) 
        if instance is not None:

            instance.delete()
            return Response({"status": "success", "message": "Deleted successfully", "response_code": status.HTTP_200_OK})
        else:
               return Response({"status": "error", "message": "Turf does not exist", "response_code": status.HTTP_404_NOT_FOUND})
    
    def patch(self, request, pk):
        instance = self.get_instance(pk)
        if instance is not None:

            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
               return Response({"status": "error", "message": "Turf does not exist", "response_code": status.HTTP_404_NOT_FOUND})
    
      

class CustomerList(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})


class CustomerListDelete(generics.RetrieveDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer
    def get_instance(self, pk):
        try:
            return self.get_queryset().get(pk=pk)
        except Customer.DoesNotExist:
            return None

    def get(self,request,pk):
        instance = self.get_instance(pk)
        if instance is not None:

            serializer = self.get_serializer(instance)
            return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})
        else:
               return Response({"status": "error", "message": "Customer does not exist", "response_code": status.HTTP_404_NOT_FOUND})
    
    def delete(self, request, pk):
        instance = self.get_instance(pk)
        if instance is not None:

            instance.delete()
            return Response({"status": "success", "message": "User deleted Successfully", "response_code": status.HTTP_200_OK})
        else:
               return Response({"status": "error", "message": "Customer does not exist", "response_code": status.HTTP_404_NOT_FOUND})
    

class TurfBookingView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = TurfBooking.objects.all()
    serializer_class = BookingSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})
    

class TurfBookingCancel(generics.RetrieveDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = TurfBooking.objects.all()
    serializer_class = BookingSerializer
    def get_instance(self, pk):
        try:
            return self.get_queryset().get(pk=pk)
        except TurfBooking.DoesNotExist:
            return None

    def get(self,request,pk):
        instance = self.get_instance(pk)
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})
        else:
               return Response({"status": "error", "message": "Booking does not exist", "response_code": status.HTTP_404_NOT_FOUND})
    
    def delete(self, request,pk):
        instance = self.get_instance(pk)
        if instance is not None:
            instance.delete()
            return Response( {"status": "success", "message": "Turf booking cancelled", "response_code" :status.HTTP_200_OK})
        else:
               return Response({"status": "error", "message": "Booking does not exist", "response_code": status.HTTP_404_NOT_FOUND})
    

class TransactionHistory(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = PaymentHistoryModel.objects.all()
    serializer_class = TransactionHistorySerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})
      


class AdminIncomeView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

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
            'start_date': start_date.strftime('%d-%m-%Y'),
            'end_date': end_date.strftime('%d-%m-%Y')
        }
        
        return Response({"status": "success", "message": data, "response_code": status.HTTP_200_OK})

    def calculate_income(self, start_date, end_date):
        total_income = TurfBooking.objects.filter(
            date__range=[start_date, end_date]
        ).aggregate(total=Sum('price'))['total'] or 0

        return total_income
    
    def get(self, request):
        
        # Calculate monthly income
        current_date = datetime.now()
        first_day = current_date.replace(day=1)
        last_day = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        monthly_income = TurfBooking.objects.filter(
            date__range=[first_day, last_day]).aggregate(total=Sum('price'))['total'] or 0
        # monthly_balance_amount = TurfBooking.objects.filter(
        #     date__range=[first_day, last_day]).aggregate(total=Sum('balance'))['total'] or 0

        # Calculate yearly income
        year_first_day = current_date.replace(month=1, day=1)
        year_last_day = current_date.replace(month=12, day=31)
        yearly_income = TurfBooking.objects.filter(
            date__range=[year_first_day, year_last_day]).aggregate(total=Sum('price'))['total'] or 0
        # yearly_balance_amount = TurfBooking.objects.filter(
        #     date__range=[year_first_day, year_last_day]).aggregate(total=Sum('balance'))['total'] or 0

        data = {
            'monthly_income': monthly_income,
            'total_income': yearly_income,
            # 'monthly_balance_amount':monthly_balance_amount,
            # 'yearly_balance_amount':yearly_balance_amount
        }
        
        return Response({"status": "success", "message": data, "response_code": status.HTTP_200_OK})




    


#   ///// AI

from django.db.models import  Value,DateField

class TurfWeeklyIncomeView(APIView):
    def get(self, request):
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        weekly_income = []

        for i in range(52):  
            start_date = start_of_week - timedelta(weeks=i)
            end_date = end_of_week - timedelta(weeks=i)
            income = TurfBooking.objects.filter(
                date__range=[start_date, end_date]).values('turf__id', 'turf__name').annotate( start_date=Value(start_date, output_field=DateField()),
                end_date=Value(end_date, output_field=DateField()),
                total_income=Sum('price'),total_booking=Count('id'), )

            weekly_income.extend(list(income))

        filtered_income = [
            entry for entry in weekly_income 
            if entry['turf__id'] is not None 
        ]
    
        return Response({"status": "success", "message": filtered_income, "response_code": status.HTTP_200_OK})



#   //////////////////    AI 
# 
# 
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta 


class TurfMonthlyIncomeView(APIView):
    def get(self, request):
        today = datetime.now()
        start_of_month = today.replace(day=1)

        start_of_previous_month = start_of_month - relativedelta(months=1)
        end_of_previous_month = start_of_month - timedelta(days=1)
        monthly_income = []

        income = TurfBooking.objects.filter(
                date__range=[start_of_previous_month, end_of_previous_month]
            ).values('turf__id', 'turf__name','turf__price','turf__owner').annotate(total_income=Sum('price'),total_booking=Count('id'),)


        monthly_income.extend(list(income))
        filtered_income = [
            entry for entry in monthly_income 
            if entry['turf__id'] is not None 
        ]
        return Response({"status": "success", "message": filtered_income, "response_code": status.HTTP_200_OK})




class TeamLeaderBoard(generics.ListAPIView):
    serializer_class = LeaderBoardSerializer

    def get_queryset(self):
        queryset = Leaderboard.objects.filter(win_ratio__gt=0).order_by('-win_ratio','-aggregate_score_ratio')[:4]
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})


# class PlayerLeaderBoard(generics.ListAPIView):
#     serializer_class = PlayerLeaderBoardSerializer

#     def get_queryset(self):
#         queryset = Player.objects.annotate(no_of_win=Count('team__leaderboard__number_of_wins')).order_by('-no_of_win')
#         return queryset

#     def list(self, request):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})



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
    def get_instance(self, pk):
        try:
            return self.get_queryset().get(pk=pk)
        except Amenity.DoesNotExist:
            return None

    def get(self,request, pk):
        instance = self.get_instance(pk)
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})
        else:
               return Response({"status": "error", "message": "Amenity does not exist", "response_code": status.HTTP_404_NOT_FOUND})
    
    def delete(self, request, pk):
        instance = self.get_instance(pk)
        if instance is not None:
            instance.delete()
            return Response({"status": "success", "message": "Deleted successfully", "response_code": status.HTTP_200_OK})
        else:
            return Response({"status": "error", "message": "Amenity does not exist", "response_code": status.HTTP_404_NOT_FOUND})
    
    

class RewardView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    def get_instance(self, pk):
        try:
            return self.get_queryset().get(pk=pk)
        except Reward.DoesNotExist:
            return None

    def get(self,request, pk):
        instance = self.get_instance(pk)
        if instance is not None:
           serializer = self.get_serializer(instance)
           return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})
        else:
            return Response({"status": "error", "message": "Reward does not exist", "response_code": status.HTTP_404_NOT_FOUND})
    
    def delete(self, request, pk):
        instance = self.get_instance(pk) 
        if instance is not None:
           instance.delete()
           return Response({"status": "success", "message": "Deleted successfully", "response_code": status.HTTP_200_OK})
        else:
            return Response({"status": "error", "message": "Reward does not exist", "response_code": status.HTTP_404_NOT_FOUND})
    
    def patch(self, request, pk):
        instance = self.get_instance(pk)
        if instance is not None:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", 
                                 "message": serializer.data, "response_code": status.HTTP_200_OK})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": "error", "message": "Reward does not exist",
                              "response_code": status.HTTP_404_NOT_FOUND})
    


from geopy.distance import distance 
from django.shortcuts import get_object_or_404

class TurfDisplayView(generics.RetrieveAPIView):
    serializer_class = TurfSerializer

    def get_queryset(self):
        pk = self.kwargs.get('id')  
        user = Customer.objects.get(pk=pk)

        customer_latitude = float(user.customer.latitude)
        customer_longitude = float(user.customer.longitude)
       
        customer_location = (customer_latitude, customer_longitude)
        
        all_turfs = Turf.objects.all() 
        
        turf_distances = {
            turf: distance(customer_location, (turf.latitude, turf.longitude)).km
            for turf in all_turfs
        }
       
        sorted_turfs = sorted(turf_distances, key=turf_distances.get)
        # dist = distance(customer_location, (turf_lati, turf_longi)).miles
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
    queryset = Customer.objects.all()

    def get_intance(self,pk):
        try:
            
            return self.get_queryset().get(pk=pk)
        except Customer.DoesNotExist:
            return None

    # def get_object(self):
    #     return self.request.user 

    def patch(self, request, pk):
        instance = self.get_intance(pk)
        if instance is not None:

            serializer = self.get_serializer(instance, data=request.data, partial=True)
        
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "message": serializer.data, "response_code": status.HTTP_200_OK})

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": "error", "message": "User does not exist", "response_code": status.HTTP_404_NOT_FOUND})
    



class NearByTurf(APIView):
    def get(self, request):
        try:

           latitude_str = self.request.query_params.get('latitude')
           longitude_str = self.request.query_params.get('longitude')
        #    latitude_str = 40.7128
        #    longitude_str = 74.0060
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
                'rating':turf.ai_rating,
                'distance_km': distance(user_location, (turf.latitude, turf.longitude)).km
            })

           sorted_turfs = sorted(turf_data, key=lambda x: x['distance_km'])
           return Response({"status": "success", "response_code": status.HTTP_200_OK, "message": sorted_turfs})
        except (ValueError, TypeError):
            return Response({"status": "error", "response_code": status.HTTP_400_BAD_REQUEST, "message": "Invalid latitude or longitude"}, status=status.HTTP_400_BAD_REQUEST)


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

                # if team1_id is not None and match_id is not None:             
                response_data.append({
                    'match_id':match_id,
                    'team_id' : team1_id ,
                    'result': team1_result,
                    'date': date_played,
                    'players':team1_players
                   })
                # if team1_id is not None and match_id is not None:             
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
    def get(self, request, turf_id):
        ai_backend_url = 'https://cadc-116-68-110-250.ngrok-free.app/inco/income'

        try:
            response = requests.get(ai_backend_url)
            response.raise_for_status()
            
            income_data = response.json()
            turf_income = None
            for income in income_data:
                if turf_id == income.get('turf__id'):
                    turf_income = income
                    break
                      
            return Response({"status": "success", "message": turf_income,"response_code": status.HTTP_200_OK})
            
        except requests.RequestException:
            return Response({"status": "failure", "message": "Request failed: "})            



class DisplayWeeklyBookingData(APIView):
    def get(self, request, turf_id):
        ai_backend_url = 'https://cadc-116-68-110-250.ngrok-free.app/book/booking'

        try:
            response = requests.get(ai_backend_url)
            response.raise_for_status()
            
            booking_data = response.json()
            turf_booking = None
            for booking in booking_data:
                if turf_id == booking.get('turf__id'):
                    turf_booking = booking
                    
            return Response({"status": "success", "message": turf_booking,"response_code": status.HTTP_200_OK})
        
        except requests.RequestException:
            return Response({"status": "failure", "message": "Request failed "})            



class AvailableTurf(APIView):

    def get(self, request):
        user_selected_date_str = request.query_params.get('user_selected_date')
        user_selected_start_time_str = request.query_params.get('user_selected_start_time')
        user_selected_end_time_str = request.query_params.get('user_selected_end_time')

        user_selected_date = datetime.strptime(user_selected_date_str, "%Y-%m-%d")
        user_selected_start_time = datetime.strptime(user_selected_start_time_str, "%H:%M:%S")
        user_selected_end_time = datetime.strptime(user_selected_end_time_str, "%H:%M:%S")

        # user_selected_date = datetime.strptime("2023-12-13", "%Y-%m-%d")
        # user_selected_start_time = datetime.strptime("09:00:00", "%H:%M:%S")
        # user_selected_end_time = datetime.strptime("11:00:00", "%H:%M:%S")
        conflict_booking = TurfBooking.objects.filter(
            date=user_selected_date,
            start_time__lt=user_selected_end_time,
            end_time__gt=user_selected_start_time
        )
        conflict_turf =   conflict_booking.values_list('turf_id',flat=True)  
        available_turf = Turf.objects.exclude(id__in=conflict_turf)  

       
        try:
            # latitude_str = request.query_params.get('latitude')
            # longitude_str = request.query_params.get('longitude')
            latitude_str = 40.7128
            longitude_str = 74.0060
            latitude = float(latitude_str)
            longitude = float(longitude_str)
            user_location = (latitude, longitude)
        
            turf_data = []
            for turf in available_turf:
                amenities = [amenity.name for amenity in turf.amenity.all()]
                image_url = request.build_absolute_uri(turf.image.url)
                distance_km = distance(user_location, (turf.latitude, turf.longitude)).km

                turf_data.append({
                'id': turf.id,
                'name': turf.name,
                'location': turf.location,
                'price': turf.price,
                'image': image_url,
                'description': turf.description,
                'amenities': amenities,
                'distance_km': distance_km
            })

            sorted_turfs = sorted(turf_data, key=lambda x: x['distance_km'])

            # available_turf_data = list(available_turf.values())
            return Response({"status": "success", "response_code": status.HTTP_200_OK, "message": sorted_turfs})
        except (ValueError, TypeError):
            return Response({"status": "error", "response_code": status.HTTP_400_BAD_REQUEST, "message": "Invalid latitude or longitude"}, status=status.HTTP_400_BAD_REQUEST)

        # return Response(available_turf_data)



class User_Team_Search(APIView):
    def get(self, request):
        try:
           latitude_str = self.request.query_params.get('latitude')
           longitude_str = self.request.query_params.get('longitude') 
        
        #    latitude_str = 11.2514
        #    longitude_str = 75.7804
           latitude = float(latitude_str)
           longitude = float(longitude_str)
           user_location = (latitude, longitude)
           all_teams = Team.objects.all() 

           team_data = []
           for team in all_teams:
               image_url = request.build_absolute_uri(team.team_pic.url)  

               team_data.append({
                'id': team.id,
                'name': team.team_name, 
                'skill': team.team_skill,
                'strength': team.team_strength,
                'image': image_url,
                'distance_km': distance(user_location, (team.team_latitude, team.team_longitude)).km
            })

           sorted_team = sorted(team_data, key=lambda x: x['distance_km'])
           return Response({"status": "success", "response_code": status.HTTP_200_OK, "message": sorted_team})
        except (ValueError, TypeError):
            return Response({"status": "error", "response_code": status.HTTP_400_BAD_REQUEST, "message": "Invalid latitude or longitude"}, status=status.HTTP_400_BAD_REQUEST)



class User_Player_Search(APIView):
    def get(self, request):
        try:
           latitude_str = self.request.query_params.get('latitude')
           longitude_str = self.request.query_params.get('longitude') 
        
        #    latitude_str = 11.2514
        #    longitude_str = 75.7804
           latitude = float(latitude_str)
           longitude = float(longitude_str)
           user_location = (latitude, longitude)
           all_players = Player.objects.all() 

           player_data = []
           for player in all_players:
               image_url = request.build_absolute_uri(player.player_pic.url)  
               player_teams = [team.team_name for team in player.teams.all()]  # Fetch teams associated with the player

               player_data.append({
                'id': player.id,
                'name': player.player_name, 
                'skill': player.player_skill,
                'strength': player.player_position,
                'image': image_url,
                'teams': player_teams,
                'distance_km': distance(user_location, (player.player_latitude, player.player_longitude)).km
            })

           sorted_player = sorted(player_data, key=lambda x: x['distance_km'])
           return Response({"status": "success", "response_code": status.HTTP_200_OK, "message": sorted_player})
        except (ValueError, TypeError):
            return Response({"status": "error", "response_code": status.HTTP_400_BAD_REQUEST, "message": "Invalid latitude or longitude"}, status=status.HTTP_400_BAD_REQUEST)



class playersLeaderBoard(APIView):
    def get(self, request):
        ai_backend_url = 'https://cadc-116-68-110-250.ngrok-free.app/prob/playerdata'

        try:

            response = requests.get(ai_backend_url)
            response.raise_for_status()
            
            player_data = response.json()
            player_ids = [player['Player'] for player in player_data]  

            players = Player.objects.filter(id__in=player_ids)
    
            matching_players = []
            for player_info in player_data:
                player_id = player_info['Player']
                player = players.filter(id=player_id).first()

                if players.filter(id=player_id).exists():
                    if player and player_info['Win_Count'] > 0:

                        player_info['image'] = request.build_absolute_uri(player.player_pic.url)
                        player_info['name'] = player.player_name
                        player_info['skill']=player.player_skill
                        matching_players.append(player_info)
            matching_players.sort(key=lambda x: x['win_ratio'], reverse=True)
            top_four_players = matching_players[:4]
            return Response({"status": "success", "message": top_four_players,"response_code": status.HTTP_200_OK})
        
        except requests.RequestException:
            return Response({"status": "failure", "message": "Request failed: "})            




class CustomerBookingCount(APIView):
   
    def get(self, request):
        queryset = TurfBooking.objects.filter(
            date__gte=timezone.now() - timedelta(days=90)
        ).values('user').annotate(booking_count=Count('user'))

        data = list(queryset) 

        return Response({
            "status": "success",
            "message": data,
            "response_code": status.HTTP_200_OK
        })

    
    


class NotificationToOwner(APIView):
    def get(self, request, owner__id):
        ai_backend_url = 'https://9951-116-68-110-250.ngrok-free.app/anom/send_notifications'

        try:
            response = requests.get(ai_backend_url)
            response.raise_for_status()
            
            notifications = response.json()
            owner_notification = None

            for msg in notifications:
                turfname = msg.get('turf_name')
                owner_id = msg.get('owner_id')
                message = msg.get('message')
                # owner_notification = None
                if owner__id == owner_id: 
                    owner_notification = {
                        "owner_id" : owner_id,
                        "turf_name":turfname,
                        "message": message
                    }
                    break
                    # return Response({"status": "success", "message": owner_notification,"response_code": status.HTTP_200_OK})
            if owner_notification:
                return Response({"status": "success", "message": owner_notification, "response_code": status.HTTP_200_OK})
            else:
                return Response({"status": "success", "message": None, "response_code": status.HTTP_200_OK})    

        except requests.RequestException:
            return Response({"status": "failure", "message": "Request failed: "})            

   


# from geopy.geocoders import Nominatim

# def get_lat_lng(location_name):
#     try:
#         geolocator = Nominatim(user_agent="my_geocoder")  
#         location = geolocator.geocode(location_name)

#         if location:
#             return location.latitude, location.longitude
#         else:
#             return None
#     except Exception as e:
#         print("Error:", e)
#         return None

# # Usage
# location = "calicut"
# coordinates = get_lat_lng(location)
# if coordinates:
#     print(f"Latitude: {coordinates[0]}, Longitude: {coordinates[1]}")
# else:
#     print("Location not found or error occurred.")
