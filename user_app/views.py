from django.http import Http404
from django.shortcuts import render
from rest_framework import generics, status ,mixins, permissions
from . models import *
from . serializers import *
from owner_app.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from geopy.distance import distance
from rest_framework .authtoken.models import Token
from . help import *
import requests
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta



# Create your views here.
class CustomerRegistrationView(generics.CreateAPIView):
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
    serializer_class = TurfBookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return TurfBooking.objects.filter(turf=pk)

    def perform_create(self, serializer):
        user = self.request.user
        turf = self.kwargs['pk'] 

        try:
            selected_turf = Turf.objects.get(pk=turf)
        except Turf.DoesNotExist:
            raise Http404("Turf does not exist")

        if isinstance(user, Customer):
            serializer.validated_data['user'] = user
        else:
            customer = Customer.objects.get(customer=user)
            serializer.validated_data['user'] = customer

        serializer.validated_data['turf'] = selected_turf

        serializer.save()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            'status': "success",
            'message': "Booking successful",
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        })
    
class TurfBookingAIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TurfBookingAISerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')
        user_id = user.id
        print("user id is", user_id)
        if user_id is None:
            return Response({'error': 'User ID not provided in the request data'}, status=status.HTTP_400_BAD_REQUEST)

        date_obj = serializer.validated_data.get('date')
        start_time_obj = serializer.validated_data.get('start_time')
        end_time_obj = serializer.validated_data.get('end_time')
        price = serializer.validated_data.get('price')
        turf = serializer.validated_data.get('turf')
        turf_id = turf.id

        formatted_date = date_obj.strftime('%Y-%m-%d')
        formatted_start_time = start_time_obj.strftime('%H:%M:%S')
        formatted_end_time = end_time_obj.strftime('%H:%M:%S')

        ai_endpoint = 'https://043e-116-68-110-250.ngrok-free.app/dynamic_discount'
        print("ai is price is ", price)
        three_months = datetime.now() - timedelta(days=90)

        booking_count = TurfBooking.objects.filter(user=user_id, date__gte=three_months).count()
        print("BOOKING COUNT IN LAST 3 MONTHS IS ", booking_count)
        ai_data = {
            'user': user_id,
            'date': formatted_date,
            'start_time': formatted_start_time,
            'end_time': formatted_end_time,
            'price': price,
            'turf': turf_id,
            'booking_count':booking_count
        }

        # Initialize ai_response here
        ai_response = None

        try:
            # Make a POST request to the AI service
            ai_response = requests.post(ai_endpoint, json=ai_data)
            ai_response.raise_for_status()  # Raise an exception for bad responses

            # Check if 'dpiscount_price' key is present in the JSON response
            if 'discount_price' in ai_response.json():
                # Get the modified price from the AI service response
                modified_price = ai_response.json()['discount_price']
                print("modified price is ", modified_price)

                # Create a new AiTurfBookModel instance with the modified price
                AiTurfBookModel.objects.create(
                    user=user,
                    date=date_obj,
                    start_time=start_time_obj,
                    end_time=end_time_obj,
                    price=modified_price,
                    turf=turf
                )

                # Return the modified price to the frontend
                return Response({'modified_price': modified_price, 'date': date_obj, 'start_time': start_time_obj,
                                 'end_time': end_time_obj, 'turf': turf.id, 'user': user.id},
                                status=status.HTTP_200_OK)
            else:
                # Print the entire response content for debugging
                print(f"Unexpected response format. Response content: {ai_response.content}")

                # Handle the case where 'discount_price' key is not present
                return Response({'error': 'Invalid response format'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except requests.RequestException as e:
            # Log the error and print the response content
            print(f"Error: {str(e)}")
            print(f"Response content: {ai_response.content if ai_response else 'No response'}")

            # Return a more informative response
            return Response({'error': 'Error making request to AI service'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except requests.RequestException as e:
            # Log the error and print the response content
            print(f"Error: {str(e)}")
            print(f"Response content: {ai_response.content}")

            # Return a more informative response
            return Response({'error': 'Error making request to AI service'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
    
    def post(self, request):
        serializer = TeamSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': "success",
                            'message': "Team adding Successful",
                            'response_code': status.HTTP_200_OK,
                            'data': serializer.data})
        else:
            data = serializer.errors
            return Response({'status': "error",
                            'message': "Team adding failed",
                            'response_code': status.HTTP_404_NOT_FOUND, 
                            'data': data})
        
    
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
            data = serializer.errors
            return Response({'status': "error",
                            'message': "Team fetching unsuccessful",
                            'response_code': status.HTTP_404_NOT_FOUND,
                            'data': data})
        
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
                data = serializer.errors
                return Response({'status': "error",
                                'message': "updation unsuccessful",
                                'response_code': status.HTTP_403_FORBIDDEN,
                                'data': data})
        else:
            data = serializer.errors
            return Response({'status': "error",
                            'message': "not found",
                            'response_code': status.HTTP_404_NOT_FOUND,
                            'data': data})
        
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
                        'team_strength': team_strength,
                        'data': serializer.data
                    }
                    Response(response_data)
            else:
                # return Response({'status': "error",
                #                 'message': "not found",
                #                 'response_code': status.HTTP_404_NOT_FOUND})
                response_data = {
                        'status': "error",
                        'message': 'Team not found',
                        'response_code': status.HTTP_404_NOT_FOUND
                        }
                raise serializers.ValidationError(response_data)
        else:
            serializer.save()
            response_data = {
                'status': "success",
                'message': 'Saved without team ID',
                'response_code': status.HTTP_200_OK
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
            data = serializer.errors
            return Response({'status': "error",
                            'message': "Unable to get player",
                            'response_code': status.HTTP_403_FORBIDDEN,
                            'data': data})
        
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
            data = serializer.errors
            return Response({'status': "error",
                                'message': "updation unsuccessful",
                                'response_code': status.HTTP_403_FORBIDDEN,
                                'data': data})
            
        
    def delete(self,request,name):
        self.queryset = self.queryset.filter(id = name).first()
        self.perform_destroy(self.queryset)
        return Response({'status': "success",
                         'message': "deleted successfully",
                         'response_code': status.HTTP_204_NO_CONTENT})
        
        
        
class GalleryView(generics.ListCreateAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    # permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        gallery = Gallery.objects.all()
        serializers = GallerySerializer(gallery, many=True)
        return Response(serializers.data)
    
    def post(self,request):
        serializer = GallerySerializer(data=request.data)
        if serializer.is_valid():
            # serializer.validated_data['user'] = request.user
            serializer.save()
            print(request.user)
            return Response({'status': "success",
                             'message': "Image uploaded successfully",
                             'response_code': status.HTTP_200_OK})
        else: 
            data = serializer.errors
            return Response({'status': "error",
                            'message': "Image uploading unsuccessful",
                            'response_code': status.HTTP_200_OK,
                            'data': data})
            
        
class ProfileUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        print(user)

        # Retrieve Abstract and Profile instances
        abstract_instance = Abstract.objects.get(pk=user.pk)
        print(abstract_instance)
        profile_instance = Profile.objects.get(user=user)
        print(profile_instance)

        # Serialize Abstract and Profile instances
        abstract_serializer = AbstractSerializer(abstract_instance)
        profile_serializer = ProfileSerializer(profile_instance)
        return Response({'status': "success",
                        'message': "PRofile fetching Successful",
                        'response_code': status.HTTP_200_OK,
                        'abstract': abstract_serializer.data,
                        'profile': profile_serializer.data})

    def put(self, request, *args, **kwargs):
        user = request.user

        # Get or create Abstract instance
        abstract_instance, created = Abstract.objects.get_or_create(pk=user.pk, defaults={'user': user})

        serializer = ProfileCombinedSerializer(data=request.data)
        if serializer.is_valid():
            abstract_data = serializer.validated_data.get('abstract', {})
            profile_data = serializer.validated_data.get('profile', {})

            Abstract.objects.update_or_create(pk=abstract_instance.pk, defaults=abstract_data)
            Profile.objects.update_or_create(user=user, defaults=profile_data)

            return Response({'status': "success",
                            'message': "Profile updating Successful",
                            'response_code': status.HTTP_200_OK,
                            'data': serializer.data})
        else:
            data = serializer.errors
            return Response({'status': "error",
                            'message': "Profile updating unsuccessful",
                            'response_code': status.HTTP_400_BAD_REQUEST,
                            'data': data})
            
            
# class SendInvitationView(generics.CreateAPIView):
#     serializer_class = InvitationSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         team_id = serializer.validated_data['team_id']
#         player_id = serializer.validated_data['player_id']

#         try:
#             team = Team.objects.get(id=team_id)
#             player = Player.objects.get(id=player_id)
#         except (Team.DoesNotExist, Player.DoesNotExist):
#             return Response({'detail': 'Team or Player not found'}, status=status.HTTP_404_NOT_FOUND)

#         if team.players.count() < team.team_strength:
#             # Assuming you have a field in your Player model to track invitations
#             player.invitation_pending = True
#             player.save()

#             # You might want to send a notification to the player here

#             return Response({'detail': 'Invitation sent successfully'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'detail': 'Team is already full'}, status=status.HTTP_400_BAD_REQUEST)


# class AcceptInvitationView(generics.RetrieveUpdateAPIView):
#     serializer_class = PlayerSerializer
    
#     def get_object(self):
#         player_id = self.kwargs.get('pk')
#         try:
#             return Player.objects.get(id=player_id)
#         except Player.DoesNotExist:
#             return Response({'detail': 'Team or Player not found'}, status=status.HTTP_404_NOT_FOUND)

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         print(instance)
#         team = request.data.get('team')
#         print(team)
#         print(request.data)

#         if instance.invitation_pending:
#             instance.team = Team.objects.get(id=team)
#             instance.invitation_pending = False
#             instance.save()

#             # You might want to send a notification to the team that the player has accepted the invitation

#             return Response({'detail': 'Invitation accepted successfully'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'detail': 'No pending invitation for this player'}, status=status.HTTP_400_BAD_REQUEST)

class TeamInvitationView(generics.CreateAPIView):
    serializer_class = TeamInvitationSerializer

    def create(self, request, *args, **kwargs):
        team_id = request.data.get('team')
        player_id = request.data.get('player')
        
        # user_id = request.data.get('user')  # Add user ID to the request data

        try:
            team = Team.objects.filter(pk=team_id).first()
            player = Player.objects.filter(pk=player_id).first()
            # user = Player.objects.get(pk=user_id)  # Fetch the user
            my_team_players = team.players.all()
            print(my_team_players)
        except (Team.DoesNotExist, Player.DoesNotExist):
            return Response({"error": "Invalid team, player, or user ID"}, status=status.HTTP_400_BAD_REQUEST)

        if team.players.count() >= team.team_strength:
            team_under = team.players.count()
            print(team_under)
            return Response({"error": "Team is full"}, status=status.HTTP_400_BAD_REQUEST)

        if team.players.filter(pk=player_id).exists():
            return Response({"error": "Player is already in the team"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user sending the invitation is a team member
        # if user not in team.players.all():
        #     return Response({"error": "You are not a member of this team"}, status=status.HTTP_403_FORBIDDEN)

        invitation = TeamInvitation.objects.create(team=team, player=player)
        return Response({"invitation_id": invitation.id}, status=status.HTTP_201_CREATED)

class AcceptInvitationView(generics.UpdateAPIView):
    queryset = TeamInvitation.objects.all()
    serializer_class = TeamInvitationSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)

        if instance.is_accepted:
            return Response({"error": "Invitation has already been accepted"}, status=status.HTTP_400_BAD_REQUEST)
        instance.team.players.add(instance.player)
        player_instance = instance.player
        team_instance = instance.team
        print(team_instance)
        print(player_instance)
        instance.is_accepted = True
        print('HI')
        instance.save()


        return Response({"message": "Invitation accepted"}, status=status.HTTP_200_OK)
        
class RewardPoints(generics.ListAPIView):
    serializer_class = RewardPointSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return RewardPointModel.objects.filter(booking_user_pk=pk)
    
    def list(self,request , *args, **kwargs):
        user = self.kwargs['pk']
        reward_points = RewardPointModel.objects.filter(booking_user_pk=user).aggregate(total_points=models.Sum('reward_points'))
        
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