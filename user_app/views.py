from django.shortcuts import render
from rest_framework import generics, status, mixins
from . models import *
from . serializers import *
from owner_app.models import *
from rest_framework.response import Response
from geopy.distance import distance
from rest_framework .authtoken.models import Token
from . help import *

# Create your views here.
class CustomerRegistrationView(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request):
        mobile = request.data.get('abstract', {}).get('phone_no')
        print(mobile)
        print(request.data)
        # if Abstract.objects.filter(phone_no = mobile).first():
        #     return Response({'status': "failed",
        #                      'message': "Mobile number already exists",
        #                      'response_code':status.HTTP_400_BAD_REQUEST})
        response = check_mobile(mobile)
        if response:
            return response
            
        email = request.data.get('abstract', {}).get('email')
        print(email)
        # if Abstract.objects.filter(email = email).first():
        #     return Response({'status': "failed",
        #                      'message': "Email already exists",
        #                      'response_code':status.HTTP_400_BAD_REQUEST})
        response = check_email(email)
        if response:
            return response
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            token, create = Token.objects.get_or_create(user=account.customer)
            token_key = token.key
            data = {
                "message": "Account Created Successfully",
                "username": account.customer.username,
                "email": account.customer.email,
                "Phone number": account.customer.phone_no,
                "token": token_key
            }
            return Response({'status': "success",
                            'message': "Registration successful",
                            'response_code': status.HTTP_200_OK,
                            'data': data})
        else:
            data = serializer.errors
            return Response({'status': "error",
                            'message': "Registration unsuccessful",
                            'response_code': status.HTTP_403_FORBIDDEN,
                            'data': data})    
    
        
class BookingView(generics.ListCreateAPIView):
    queryset = TurfBooking.objects.all()
    serializer_class = TurfBookingSerializer
    
    
    
# class TurfDisplayView(generics.ListAPIView):
#     queryset = Turf.objects.all()
#     serializer_class = TurfDisplaySerializer
    
#     def get_queryset(self):
#         user_latitude = float(self.request.query_params.get('latitude', 0))
#         user_longitude = float(self.request.query_params.get('longitude', 0))

#         user_location = (user_latitude, user_longitude)

#         turfs = Turf.objects.all()
#         turfs_with_distance = sorted(
#             turfs,
#             key=lambda turf: distance(user_location, (turf.latitude, turf.longitude)).miles
#         )
#         return turfs_with_distance
    
    
    
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
            return Response({'status': "success",
                            'message': "Team fetching Successful",
                            'response_code': status.HTTP_200_OK,
                            'data': serializer.data})
        else:
            return Response({'status': "error",
                            'message': "not found",
                            'response_code': status.HTTP_404_NOT_FOUND})
        
    def put(self, request, name):
        self.queryset = self.queryset.filter(id = name).first()
        if self.queryset:
            serializer = self.get_serializer(self.queryset, data=request.data)
            if serializer.is_valid():
                print('HI ENTERED')
                serializer.save()
                return Response({'status': "success",
                                'message': "updated successfully",
                                'response_code': status.HTTP_200_OK,
                                'data': serializer.data})
            else:
                return Response({'status': "error",
                                'message': "updation unsuccessful",
                                'response_code': status.HTTP_403_FORBIDDEN})
        else:
            return Response({'status': "error",
                            'message': "not found",
                            'response_code': status.HTTP_404_NOT_FOUND})
        
    def delete(self, request, name):
        self.queryset = self.queryset.filter(id = name).first()
        self.perform_destroy(self.queryset)
        return Response({'status': "success",
                         'message': "deleted successfully",
                         'response_code': status.HTTP_204_NO_CONTENT})
        
        
    
class PlayerView(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    
    def perform_create(self, serializer):
    # def post(self, serializer):
        print(serializer)
        team_id = self.request.data.get('team')
        print('Teamid :',team_id)
        print(self.request.data)

        if team_id:
            # team_strength = Team.objects.get(id=team_id).team_strength
            team_strength_query = Team.objects.filter(id=team_id).first()
            if team_strength_query:
                team_strength = team_strength_query.team_strength
                players_count = Player.objects.filter(team_id=team_id).count()

                if players_count >= team_strength:
                    print('checked')
                    # return Response({'status': "error",
                    #                 'message': "Team has reached the maximum number of players.",
                    #                 'response_code': status.HTTP_403_FORBIDDEN,
                    #                 'team_strength': team_strength})
                    response_data = {
                        'status': "error",
                        'message': 'Team has reached the maximum number of players.',
                        'response_code': status.HTTP_403_FORBIDDEN,
                        'team_strength': team_strength
                    }
                    raise serializers.ValidationError(response_data)
                else:
                    print('entered in else')
                    serializer.save()
                    # return Response({'status': "success",
                    #                 'message': "Player added successfully",
                    #                 'response_code': status.HTTP_200_OK,
                    #                 'team_strength': team_strength})
                    response_data = {
                        'status': "success",
                        'message': 'Player added successfully',
                        'response_code': status.HTTP_200_OK,
                        'team_strength': team_strength
                    }
                    Response(response_data)
            else:
                # return Response({'status': "error",
                #                 'message': "not found",
                #                 'response_code': status.HTTP_404_NOT_FOUND})
                response_data = {
                        'status': "error",
                        'message': 'not found',
                        'response_code': status.HTTP_404_NOT_FOUND
                        }
                raise serializers.ValidationError(response_data)
        else:
            response_data = {
                'status': "error",
                'message': 'Team ID not provided',
                'response_code': status.HTTP_400_BAD_REQUEST
            }
            raise serializers.ValidationError(response_data)
    
class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    # lookup_field = "name"
    
    def get(self, request, name):
        self.queryset = self.queryset.filter(id = name).first()
        if self.queryset:
            serializer = self.get_serializer(self.queryset)
            return Response({'data': serializer.data})
        else:
            return Response({'error': 'not found'},
                            status=status.HTTP_403_FORBIDDEN)
        
    def put(self, request, name):
        self.queryset = self.queryset.filter(id = name).first()
        serializer = self.get_serializer(self.queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': "success",
                             'message': "updated successfully",
                             'response_code': status.HTTP_200_OK,
                             'data': serializer.data})
        else:
            return Response({'error': 'not updated'},
                            status=status.HTTP_403_FORBIDDEN)
            
        
    def delete(self,request,name):
        self.queryset = self.queryset.filter(id = name).first()
        self.perform_destroy(self.queryset)
        return Response({'status': "success",
                         'message': "deleted successfully",
                         'response_code': status.HTTP_204_NO_CONTENT})
    


class RewardPoints(generics.ListAPIView):
    serializer_class = RewardPointSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return RewardPointModel.objects.filter(booking__user__pk=pk)
    
    def list(self,request , *args, **kwargs):
        user = self.kwargs['pk']
        reward_points = RewardPointModel.objects.filter(booking__user__pk=user).aggregate(total_points=models.Sum('reward_points'))
        
        if not reward_points['total_points']:
            total_points = 0
        else:
            total_points = reward_points['total_points']
            
        response_data = {
            'user': user,
            'total_points': total_points,
            'reward_points': self.serializer_class(self.get_queryset(), many=True).data
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
    
    
class UserBookingHistoryView(generics.ListAPIView):
    serializer_class = UserBookingHistorySerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return UserBookingHistory.objects.filter(user=pk)
    
    
class RedeemRewards(generics.CreateAPIView):
    serializer_class = RedeemRewardsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        reward = serializer.validated_data.get('reward') 

        if not reward or user.reward_points < reward.reward_points:
            return Response({'status': "failed",'message': 'Not enough reward points or invalid reward','response_code':status.HTTP_400_BAD_REQUEST})

        instance = serializer.save(redeemed_date=timezone.now())

        user.reward_points -= reward.reward_points
        user.save()
        response_data = {
                        'user': user.customer.username,
                        'redeemed_reward': reward.reward_name,
                        'redeemed_date': instance.redeemed_date if instance else None,
                        'remaining_points': user.reward_points,
                        }

        return Response({'status':"success",'message': "Reward redeemed successfully","data":response_data,'response_code': status.HTTP_201_CREATED,})
