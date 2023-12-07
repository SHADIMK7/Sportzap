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
    queryset = TurfBooking.objects.all()
    serializer_class = TurfBookingSerializer
    
    def post(self, request):
        serializer = TurfBookingSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': "success",
                            'message': "Booking successful",
                            'response_code': status.HTTP_200_OK,
                            'data': serializer.data})
        else:
            data = serializer.errors
            return Response({'status': "error",
                            'message': "Registration unsuccessful",
                            'response_code': status.HTTP_403_FORBIDDEN,
                            'data':data}) 
    
    
    
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

        # Retrieve Abstract and Profile instances
        abstract_instance = Abstract.objects.get(pk=user.pk)
        profile_instance = Profile.objects.get(user=user)

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
            
            
class SendInvitationView(generics.CreateAPIView):
    serializer_class = InvitationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        team_id = serializer.validated_data['team_id']
        player_id = serializer.validated_data['player_id']

        try:
            team = Team.objects.get(id=team_id)
            player = Player.objects.get(id=player_id)
        except (Team.DoesNotExist, Player.DoesNotExist):
            return Response({'detail': 'Team or Player not found'}, status=status.HTTP_404_NOT_FOUND)

        if team.players.count() < team.team_strength:
            # Assuming you have a field in your Player model to track invitations
            player.invitation_pending = True
            player.save()

            # You might want to send a notification to the player here

            return Response({'detail': 'Invitation sent successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Team is already full'}, status=status.HTTP_400_BAD_REQUEST)


class AcceptInvitationView(generics.RetrieveUpdateAPIView):
    serializer_class = PlayerSerializer
    
    def get_object(self):
        player_id = self.kwargs.get('pk')
        try:
            return Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            return Response({'detail': 'Team or Player not found'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        team = request.data.get('team')
        print(team)
        print(request.data)

        if instance.invitation_pending:
            instance.team = Team.objects.get(id=team)
            instance.invitation_pending = False
            instance.save()

            # You might want to send a notification to the team that the player has accepted the invitation

            return Response({'detail': 'Invitation accepted successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No pending invitation for this player'}, status=status.HTTP_400_BAD_REQUEST)