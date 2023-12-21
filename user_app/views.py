import requests
import stripe
from django.core.files.base import ContentFile
from django.http import Http404
from rest_framework import generics, status, permissions
from . models import *
from . serializers import *
from owner_app.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from geopy.distance import distance
from rest_framework .authtoken.models import Token
from . help import *
from . stripe_helper import *
import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from datetime import datetime, timedelta
from owner_app.permissions import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
from django.conf import settings
from rest_framework.exceptions import PermissionDenied


# Create your views here.
class CustomerRegistrationView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request):
        mobile = request.data.get('abstract', {}).get('phone_no')
        # if Abstract.objects.filter(phone_no = mobile).first():
        #     return Response({'status': "failed",
        #                      'message': "Mobile number already exists",
        #                      'response_code':status.HTTP_400_BAD_REQUEST})
        response = check_mobile(mobile)
        if response:
            return response
            
        email = request.data.get('abstract', {}).get('email')
        # if Abstract.objects.filter(email = email).first():
        #     return Response({'status': "failed",
        #                      'message': "Email already exists",
        #                      'response_code':status.HTTP_400_BAD_REQUEST})
        response = check_email(email)
        if response:
            return response
        
        serializer = self.serializer_class(data=request.data)
        password = request.data.get('abstract.password')
        email = request.data.get('abstract.email')
        if serializer.is_valid():
            account = serializer.save()
            token, create = Token.objects.get_or_create(user=account.customer)
            token_key = token.key
            data = {
                "message": "Account Created Successfully",
                "username": account.customer.username,
                "email": account.customer.email,
                "Phone number": account.customer.phone_no,
                "password" : account.customer.password,
                "token": token_key
            }
            message = render_to_string('registration.html', {'user_password': password, 'user_email': email})
            plain_message = strip_tags(message)

            subject = 'Sportzap Registration'
            from_email = settings.EMAIL_HOST_USER
            to_email = email

            email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
            email.attach_alternative(message, "text/html")
            
            with open("media/image/placeholder.png", "rb") as f:
                logo_data = f.read()
                email_image = MIMEImage(logo_data)
                email_image.add_header('Content-ID', '<logo>')
                email.attach(email_image)

            email.send()
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
    
    
class TurfAvailabilityShow(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsUserOnly]
    serializer_class = UserBookingHistorySerializer

    def get_object(self):
        pk = self.kwargs['pk']
        turf_booking_history = UserBookingHistory.objects.filter(turf_booked__turf=pk).first()
        return turf_booking_history
 
    def get(self, request, *args, **kwargs):
        turf_booking_history = self.get_object()

        user_id = self.request.user.id
        three_months_ago = datetime.now() - timedelta(days=90)

        booking_count = TurfBooking.objects.filter(user__customer=user_id, date__gte=three_months_ago).count()
        if turf_booking_history is None:
            return Response({"detail": "Turf booking history not found.","user booking count": booking_count}, status=404)


        serialized_data = self.get_serializer(turf_booking_history).data

        return Response({
            "turf booking history": serialized_data,
            "user booking count": booking_count
        })


class BookingView(generics.ListCreateAPIView):
    serializer_class = TurfBookingSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [CustomerPermission]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return TurfBooking.objects.filter(turf=pk)

    def perform_create(self, request, serializer):
        # user = 1 
        # print("PERFORM CREATE")
        user = self.request.user
        turf = self.kwargs['pk']

        try:
            selected_turf = Turf.objects.get(pk=turf)
        except Turf.DoesNotExist:
            raise Http404("Turf does not exist")

        stripe.api_key = 'sk_test_51ONT9dSB1nMhPCpjlALhOnjHuPgxdfYIRbk54BGhlmpmT1AuipFXvQnitrUMQDh8KG1nyAEBiDu0LEwGgL9K2iDE00Nkf1Joqf'
        
        data = {
            "number" : "4242424242424242",
            "exp_month" : "04",
            "exp_year" : "2024",
            "cvc" : "124"
        }
        client = Stripe()
        token = client.create_token(data)          
        
        try:
            charge = stripe.Charge.create(
                amount=serializer.validated_data['price'],
                currency='usd',
                source=serializer.validated_data['stripe_token'],
                description='Booking payment',
            )

            if charge['status'] == 'succeeded':
                if isinstance(user, Customer):
                    serializer.validated_data['user'] = user
                else:
                    customer = Customer.objects.get(customer=user)
                    serializer.validated_data['user'] = customer

                serializer.validated_data['turf'] = selected_turf
                serializer.save()

                return True
        except stripe.error.CardError as e:
            error_msg = str(e)
            raise serializers.ValidationError({'stripe_token': error_msg})

    def post(self, request, *args, **kwargs):
        turf = self.kwargs['pk']
        try:
            selected_turf = Turf.objects.get(pk=turf)
        except Turf.DoesNotExist:
            raise Http404("Turf does not exist")
        serializer = self.get_serializer(data=request.data)   
        date = request.data['date']
        start_time = request.data['start_time']
        end_time = request.data['end_time']
        price = request.data['price']
        if self.is_time_slot_booked(turf, date, start_time, end_time):
            return Response({
                'status': "error",
                'message': "Turf is already booked for the specified time slot",
                'response_code': status.HTTP_400_BAD_REQUEST,
            })
        
        user = self.request.user.id
        
        Booking_user = Abstract.objects.filter(id=user).first()
        email = Booking_user.email
        serializer.is_valid(raise_exception=True)

        Payment_type = serializer.validated_data.get('Payment_type', 'Full_payment')

        if Payment_type == 'Full_payment':
            serializer.validated_data['turf'] = selected_turf
            
            payment_successful = self.perform_create(request, serializer)

            if payment_successful:
                return Response({
                    'status': "success",
                    'message': "Booking successful",
                    'response_code': status.HTTP_200_OK,
                    'data': serializer.data
                })

            return Response({
                'status': "error",
                'message': "Payment failed",
                'response_code': status.HTTP_400_BAD_REQUEST,
            })
        elif Payment_type == 'Offline_payment':
            # print("OFFLINE_PAYMENT")
            try:
                # print("USER IS ",user)
                customer = Customer.objects.get(customer=user)
                
                # print("customer",customer)
            except Customer.DoesNotExist:
                # print("CUSTOMER MISSING")
                raise Http404("Customer does not exist")
            serializer.validated_data['turf'] = selected_turf
            serializer.validated_data['user'] = customer

            serializer.save()
            
            message = render_to_string('booking.html', {'user': Booking_user,
                                                        'date': date,
                                                        'start': start_time,
                                                        'end': end_time,
                                                        'price': price,
                                                        'turf_name': selected_turf})
            plain_message = strip_tags(message)

            subject = 'Sportzap Regarding your booking'
            from_email = settings.EMAIL_HOST_USER
            to_email = email
            
            email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
            email.attach_alternative(message, "text/html")
            
            with open("media/image/placeholder.png", "rb") as f:
                logo_data = f.read()
                email_image = MIMEImage(logo_data)
                email_image.add_header('Content-ID', '<logo>')
                email.attach(email_image)

            email.send()
            
            return Response({
                'status': "success",
                'message': "Booking successful (offline payment)",
                'response_code': status.HTTP_200_OK,
                'data': serializer.data
            })
        else:
            return Response({
                'status': "error",
                'message': "Invalid payment method",
                'response_code': status.HTTP_400_BAD_REQUEST,
            })
            
    def is_time_slot_booked(self, turf_id, date, start_time, end_time):
        try:
            selected_turf = Turf.objects.get(pk=turf_id)

            if end_time <= start_time:
                return True
            if_bookings = TurfBooking.objects.filter(
                turf=selected_turf,
                date=date,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exists()

            return if_bookings
        except Turf.DoesNotExist:
            raise Http404("Turf does not exist")
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
# class TurfBookingAIView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = TurfBookingAISerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = serializer.validated_data.get('user')
#         user_id = user.id
#         print("user id is", user_id)
#         if user_id is None:
#             return Response({'error': 'User ID not provided in the request data'}, status=status.HTTP_400_BAD_REQUEST)

#         date_obj = serializer.validated_data.get('date')
#         start_time_obj = serializer.validated_data.get('start_time')
#         end_time_obj = serializer.validated_data.get('end_time')
#         price = serializer.validated_data.get('price')
#         turf = serializer.validated_data.get('turf')
#         turf_id = turf.id

#         formatted_date = date_obj.strftime('%Y-%m-%d')
#         formatted_start_time = start_time_obj.strftime('%H:%M:%S')
#         formatted_end_time = end_time_obj.strftime('%H:%M:%S')

#         ai_endpoint = 'https://5673-116-68-110-250.ngrok-free.app/dynamic_discount'
#         print("ai is price is ", price)
#         three_months = datetime.now() - timedelta(days=90)

#         booking_count = TurfBooking.objects.filter(user=user_id, date__gte=three_months).count()
#         print("BOOKING COUNT IN LAST 3 MONTHS IS ", booking_count)
#         ai_data = {
#             'user': user_id,
#             'date': formatted_date,
#             'start_time': formatted_start_time,
#             'end_time': formatted_end_time,
#             'price': price,
#             'turf': turf_id,
#             'booking_count':booking_count
#         }

#         # Initialize ai_response here
#         ai_response = None

#         try:
#             # Make a POST request to the AI service
#             ai_response = requests.post(ai_endpoint, json=ai_data)
#             ai_response.raise_for_status()  # Raise an exception for bad responses

#             # Check if 'dpiscount_price' key is present in the JSON response
#             if 'discount_price' in ai_response.json():
#                 # Get the modified price from the AI service response
#                 modified_price = ai_response.json()['discount_price']
#                 print("modified price is ", modified_price)

#                 # Create a new AiTurfBookModel instance with the modified price
#                 AiTurfBookModel.objects.create(
#                     user=user,
#                     date=date_obj,
#                     start_time=start_time_obj,
#                     end_time=end_time_obj,
#                     price=modified_price,
#                     turf=turf
#                 )

#                 # Return the modified price to the frontend
#                 return Response({'modified_price': modified_price, 'date': date_obj, 'start_time': start_time_obj,
#                                  'end_time': end_time_obj, 'turf': turf.id, 'user': user.id},
#                                 status=status.HTTP_200_OK)
#             else:
#                 # Print the entire response content for debugging
#                 print(f"Unexpected response format. Response content: {ai_response.content}")

#                 # Handle the case where 'discount_price' key is not present
#                 return Response({'error': 'Invalid response format'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         except requests.RequestException as e:
#             # Log the error and print the response content
#             print(f"Error: {str(e)}")
#             print(f"Response content: {ai_response.content if ai_response else 'No response'}")

#             # Return a more informative response
#             return Response({'error': 'Error making request to AI service'},
#                             status=status.HTTP_500_INTERNAL_SERVER_ERROR) 



#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------
    
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
    
    
    
class TeamView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsUserOnly]
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    
    def post(self, request):
        user = self.request.user
        serializer = TeamSerializer(data = request.data)
        if serializer.is_valid():
            user_instance = Customer.objects.filter(customer_id=user.id).first()
            if user_instance:
                u = user_instance.id
                existing_team = Team.objects.filter(team_user=u).first()
                if existing_team:
                    data = serializer.errors
                    return Response({'status': "error",
                                    'message': "Team adding failed, You had a team",
                                    'response_code': status.HTTP_404_NOT_FOUND, 
                                    'data': data})

                team = serializer.save(team_user = user_instance)
                return Response({'status': "success",
                                'message': "Team adding Successful",
                                'team': team.id,
                                'response_code': status.HTTP_200_OK,
                                'data': serializer.data})
            else:
                data = serializer.errors
                return Response({'status': "error",
                                'message': "user not found",
                                'response_code': status.HTTP_404_NOT_FOUND, 
                                'data': data})
        else:
            data = serializer.errors
            return Response({'status': "error",
                            'message': "Team adding failed",
                            'response_code': status.HTTP_404_NOT_FOUND, 
                            'data': data})
        
        
# class IsTeamCreator(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.team_user.customer_id == request.user.id
    
    
class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsTeamCreator]
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    # lookup_field = "id"
    
    def get(self, request, pk):
        # self.queryset = self.queryset.filter(id = pk).first()
        self.queryset = self.get_object()
        team_id = self.queryset.id
        if self.queryset:
            serializer = self.get_serializer(self.queryset)
            return Response({'status': "success",
                            'message': "Team fetching Successful",
                            'team_id': team_id,
                            'response_code': status.HTTP_200_OK,
                            'data': serializer.data})
        else:
            data = serializer.errors
            return Response({'status': "error",
                            'message': "Team fetching unsuccessful",
                            'response_code': status.HTTP_404_NOT_FOUND,
                            'data': data})
        
    def put(self, request, pk):
        self.check_object_permissions(request, self.get_object())
        
        self.queryset = self.queryset.filter(id = pk).first()
        if self.queryset:
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
        else:
            data = serializer.errors
            return Response({'status': "error",
                            'message': "not found",
                            'response_code': status.HTTP_404_NOT_FOUND,
                            'data': data})
        
    def delete(self, request, pk):
        self.check_object_permissions(request, self.get_object())
        
        self.queryset = self.queryset.filter(id = pk).first()
        self.perform_destroy(self.queryset)
        return Response({'status': "success",
                         'message': "deleted successfully",
                         'response_code': status.HTTP_204_NO_CONTENT})


class PlayerView(generics.ListCreateAPIView):
    # permission_classes = [IsTeamCreator]
    authentication_classes = [TokenAuthentication]
    # queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    
    def get(self, request):
        queryset = Player.objects.all()
        serializer = AllPlayerSerializer(queryset, many=True)
        data = serializer.data

        return Response({
            'status': "success",
            'message': "fetched successfully",
            'response_code': status.HTTP_200_OK,
            'data': data
        })
    
    def perform_create(self, serializer):
        user = self.request.user
        customer = Customer.objects.filter(customer_id = user.id).first()
        if customer:
            existing_player = Player.objects.filter(player_user = customer).first()
            if existing_player:
                response_data = {
                    'status': "error",
                    'message': 'You can create only one player',
                    'response_code': status.HTTP_403_FORBIDDEN,
                    'data': "{}"
                }
                raise serializers.ValidationError(response_data)
        
            player_pic = self.request.data.get('player_pic')

            processed_image = process_profile_pic_with_ai(player_pic)

            if processed_image:
                processed_image_content = processed_image
                serializer.validated_data['player_pic'] = processed_image_content
                
            team_id = self.request.data.get('team')
            print(user)

            if team_id:
                team_strength_query = Team.objects.filter(id=team_id).first()
                if team_strength_query:
                    team_strength = team_strength_query.team_strength
                    players_count = Player.objects.filter(team_id=team_id).count()

                    if players_count >= team_strength:
                        response_data = {
                            'status': "error",
                            'message': f"{' Team has reached the maximum number of players. Your team strength is:', team_strength}",
                            'response_code': status.HTTP_403_FORBIDDEN,
                            'data': "{}"
                        }
                        raise serializers.ValidationError(response_data)
                    else:
                        serializer.save()
                        response_data = {
                            'status': "success",
                            'message': 'Player added successfully',
                            'team_id': team_id,
                            'response_code': status.HTTP_200_OK,
                            'data': serializer.data
                        }
                        return Response(response_data)
                else:
                    response_data = {
                        'status': "error",
                        'message': 'Team not found',
                        'response_code': status.HTTP_404_NOT_FOUND,
                        'data': "{}"
                    }
                    raise serializers.ValidationError(response_data)
            else:
                team = Team.objects.filter(team_user_id = customer).first()
                if team:
                    teams = team.id
                    print(serializer)
                    serializer.save(player_user = customer)
                    response_data = {
                        'status': "success",
                        'message': f"{'Saved to team selected'}",
                        'team_id': teams,
                        'response_code': status.HTTP_200_OK,
                        'data': serializer.data,
                    }
                    raise serializers.ValidationError(response_data)
                else: 
                    response_data = {
                        'status': "error",
                        'message': f"{'Team not found'}",
                        'response_code': status.HTTP_404_NOT_FOUND,
                        'data': {},
                    }
                    raise serializers.ValidationError(response_data)
        else:
            response_data = {
                        'status': "error",
                        'message': 'Customer not found',
                        'response_code': status.HTTP_403_FORBIDDEN,
                        'data': "{}"
                    }
            raise serializers.ValidationError(response_data)

def process_profile_pic_with_ai(player_pic):
    try:
        ai_service_endpoint = 'https://5cdd-116-68-110-250.ngrok-free.app/formation_img'
        
        files = {'image': ('player_pic.png', player_pic.read())}
        
        response = requests.post(ai_service_endpoint, files=files)

        if response.status_code == 200:
            processed_image_bytes = response.content

            processed_image_content = ContentFile(processed_image_bytes, name='processed_image.jpg')

            return processed_image_content
        else:
            return None
    except Exception as e:
        return None
    
    
# class IsPlayerCreator(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.created_by == request.user
    
class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsPlayerCreator]
    authentication_classes = [TokenAuthentication]
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    # lookup_field = "name"
    
    def get(self, request, pk):
        self.queryset = self.queryset.filter(id = pk).first()
        s = self.queryset
        print(s)
        player_id = self.queryset.id
        if self.queryset:
            serializer = self.get_serializer(self.queryset)
            return Response({'status': "success",
                            'message': "fetched successfully",
                            'player_id': player_id,
                            'response_code': status.HTTP_204_NO_CONTENT,
                            'data': serializer.data})
        else:
            data = serializer.errors
            return Response({'status': "error",
                            'message': "Unable to get player",
                            'response_code': status.HTTP_403_FORBIDDEN,
                            'data': data})
        
    def put(self, request, pk):
        self.queryset = self.queryset.filter(id = pk).first()
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
            
        
    def delete(self,request,pk):
        self.queryset = self.queryset.filter(id = pk).first()
        self.perform_destroy(self.queryset)
        return Response({'status': "success",
                         'message': "deleted successfully",
                         'response_code': status.HTTP_204_NO_CONTENT})
        
        
        
class GalleryView(generics.ListCreateAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = []
    
    def get(self, request):
        gallery = Gallery.objects.all()
        serializers = GallerySerializer(gallery, many=True)
        return Response({'status': "success",
                            'message': "fetched successfully",
                            'response_code': status.HTTP_204_NO_CONTENT,
                            'data': serializers.data})
    
    def post(self,request):
        serializer = GallerySerializer(data=request.data)
        user = request.user
        if not request.user.is_authenticated:
            return Response({'status': "error",
                            'message': "Authentication required to upload images",
                            'response_code': status.HTTP_403_FORBIDDEN,
                            'data': ''})

        if serializer.is_valid():
            # serializer.validated_data['user'] = request.user
            user_instance = Customer.objects.filter(customer_id=user.id).first()
            serializer.save(user=user_instance)
            return Response({'status': "success",
                            'message': "Image uploaded successfully",
                            'response_code': status.HTTP_200_OK,
                            'data': ''}) 
        else:
            data = serializer.errors
            return Response({'status': "error",
                            'message': "Image uploading unsuccessful",
                            'response_code': status.HTTP_403_FORBIDDEN,
                            'data': data})
            
            
        
class ProfileUpdateView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        user_id = user.id

        abstract_instance = Abstract.objects.get(pk=user.pk)
        profile_instance = Profile.objects.filter(id=user_id).first()

        abstract_serializer = UserProfileSerializer(abstract_instance)
        profile_serializer = ProfileSerializer(profile_instance)
        return Response({'status': "success",
                        'message': "PRofile fetching Successful",
                        'response_code': status.HTTP_200_OK,
                        'abstract': {
                                        **abstract_serializer.data,
                                        **profile_serializer.data
                                    }})

    def put(self, request, *args, **kwargs):
        user = request.user

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
            
            
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.check_password(serializer.validated_data['old_password']):
                request.user.set_password(serializer.validated_data['new_password'])
                request.user.save()
                return Response({'status': "success",
                            'message': "Password changed successfully.",
                            'response_code': status.HTTP_200_OK,
                            'data': serializer.data})
            else:
                return Response({'status': "error",
                            'message': "Old password is incorrect.",
                            'response_code': status.HTTP_400_BAD_REQUEST,
                            'data': "{}"})
        else:
            return Response({'status': "error",
                                'message': "validation Error",
                                'response_code': status.HTTP_400_BAD_REQUEST,
                                'data': "{}"})
            
            
# class SendInvitationView(generics.CreateAPIView):
#     serializer_class = InvitationSerializer

class UserDelete(generics.DestroyAPIView):
    
    def delete(self, request, *args, **kwargs):
        user = self.request.user

        customer = user
        if customer:
            customer.delete()
            return Response({'status': "success",
                            'message': "User deleted successfully.",
                            'response_code': status.HTTP_200_OK})
        else:
            return Response({'status': "error",
                                'message': "Customer not found",
                                'response_code': status.HTTP_400_BAD_REQUEST})

            
class TeamInvitationView(generics.CreateAPIView):
    serializer_class = TeamInvitationSerializer
    
    def create(self, request, *args, **kwargs):
        # team_id = request.data.get('team')
        user = self.request.user
        customer = Customer.objects.filter(customer_id = user.id).first()
        if not customer:
            return Response({'status': "error",
                            'message': "Invalid Customer",
                            'response_code': status.HTTP_400_BAD_REQUEST,
                            'data': ''})
            
        user_team = Team.objects.filter(team_user = customer).first()
        team_id = user_team.id
        player_id = request.data.get('player')

        try:
            team = Team.objects.filter(pk=team_id).first()
            player = Player.objects.filter(pk=player_id).first()

            if team is None or player is None:
                return Response({'status': "error",
                                'message': "Invalid team or player ID",
                                'response_code': status.HTTP_400_BAD_REQUEST,
                                'data': '{}'})

            if team.players.count() >= team.team_strength:
                return Response({'status': "error",
                                'message': "Team is full",
                                'response_code': status.HTTP_400_BAD_REQUEST,
                                'data': '{}'})

            if team.players.filter(pk=player_id).exists():
                return Response({'status': "error",
                                'message': "Player is already in the team",
                                'response_code': status.HTTP_400_BAD_REQUEST,
                                'data': '{}'})

            invitation = TeamInvitation.objects.create(team=team, player=player, user=customer)
            if invitation:
                return Response({'status': "success",
                                'message': "Invitation successfully created",
                                "invitation_id": invitation.id,
                                "user_id": customer.customer_id,
                                'response_code': status.HTTP_201_CREATED,
                                'data': '{}'})
            else:
                return Response({'status': "error",
                                'message': "Invitation Unsuccessfully",
                                'response_code': status.HTTP_400_BAD_REQUEST,
                                'data': '{}'})

        except (Team.DoesNotExist, Player.DoesNotExist):
            return Response({'status': "error",
                            'message': "Invalid team or player ID",
                            'response_code': status.HTTP_400_BAD_REQUEST,
                            'data': '{}'})

class AcceptInvitationView(generics.UpdateAPIView):
    queryset = TeamInvitation.objects.all()
    serializer_class = TeamInvitationSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.is_accepted:
            return Response({'status': "error",
                            'message': "Invitation has already been accepted",
                            'response_code': status.HTTP_400_BAD_REQUEST,
                            'data': ''})
        instance.team.players.add(instance.player)
        instance.is_accepted = True
        instance.save()

        return Response({'status': "success",
                            'message': "Invitation accepted",
                            'response_code': status.HTTP_200_OK,
                            'data': ''})
    
    
class MatchInvitationView(generics.CreateAPIView):
    serializer_class = MatchInvitationSerializer
    
    def create(self, request, *args, **kwargs):
        
        # data=request.data
        # data['sender_team']
        
        team1_id = request.data.get('sender_team')
        team2_id = request.data.get('receiver_team')
        
        try:
            team1 = Team.objects.filter(pk = team1_id).first()
            team2 = Team.objects.filter(pk = team2_id).first()
            team1_players = team1.players.all()
            team2_players = team2.players.all()
            
            team1_user = team1.team_user.id
            team2_user = team2.team_user.id
                
            common_player = set(team1_players.values_list('id', flat=True)).intersection(team2_players.values_list('id', flat=True))

        except(Team.DoesNotExist):
            return Response({'status': "error",
                            'message': "Invalid team",
                            'response_code': status.HTTP_400_BAD_REQUEST,
                            'data': ''})
            
        if team1_user == team2_user:
            return Response({'status': "error",
                            'message': "Selected users are same",
                            'response_code': status.HTTP_400_BAD_REQUEST,
                            'data': ''})
        
        if team1_id == team2_id:
            return Response({'status': "error",
                            'message': "Selected teams are same",
                            'response_code': status.HTTP_400_BAD_REQUEST,
                            'data': ''})
        
        if common_player:
            return Response({'status': "error",
                            'message': "Selected teams have same players",
                            'response_code': status.HTTP_400_BAD_REQUEST,
                            'data': ''})
        
        if team1.team_strength == team2.team_strength:
            
            team_invitation = MatchInvitation.objects.create(sender_team = team1, receiver_team = team2)
            return Response({'status': "success",
                            'message': "invitation successfully",
                            "invitation_id": team_invitation.id,
                            'response_code': status.HTTP_201_CREATED,
                            'data': ''})
        else:
            return Response({'status': "error",
                            'message': "team strength is not same, invitation unsuccessfully",

                            'response_code': status.HTTP_400_BAD_REQUEST,
                            'data': ''})
    
class MatchAcceptInvitationView(generics.UpdateAPIView):
    queryset = MatchInvitation.objects.all()
    serializer_class = MatchInvitationSerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_accepted:
            return Response({'status': "error",
                            'message': "Invitation has already been accepted",
                            'response_code': status.HTTP_400_BAD_REQUEST,
                            'data': ''})
        else:
            instance.team1 = instance.sender_team
            instance.team2 = instance.receiver_team
            instance.is_accepted = True
            instance.save()
            return Response({'status': "success",
                            'message': "Invitation accepted",
                            'response_code': status.HTTP_200_OK,
                            'data': ''})
 
class TurfRatingView(generics.ListAPIView):
    queryset = TurfRating.objects.all()
    serializer_class = TurfRatingSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        custom_response = {
            'status': "success",
            'message': "Rating saved",
            'response_code': status.HTTP_200_OK,
            'data': serializer.data
        }
        return Response(custom_response)
 
class CreateTurfRating(generics.ListCreateAPIView):
    authentication_classes=[TokenAuthentication]
    queryset = TurfRating.objects.all()
    serializer_class = TurfRatingSerializer
    
    # def get(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = TurfRatingSerializer(queryset, many=True)
    #     return Response(serializer.data)
    def get_queryset(self):
        pk = self.kwargs['pk']
        return TurfRating.objects.filter(turfid=pk)
    
    def create(self, request, *args, **kwargs):
        # data = request.data
        user = self.request.user.id
        # user = data.get('userid')
        turf_id = self.kwargs['pk']
        print(turf_id)
        request.data['turfid'] = turf_id
        request.data['userid'] = user
        if user:
            turf = Turf.objects.filter(id=turf_id).first()
            serializer = TurfRatingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                
                ai_url = "https://1a23-116-68-110-250.ngrok-free.app/sent/sentiment"
                ai_response = requests.get(ai_url).json()
                print(ai_response)
                
                turf_rating_data = [item for item in ai_response if item.get('turfid') == int(turf_id)]
                print(turf_rating_data)


                if turf_rating_data and 'weighted_rating' in turf_rating_data[0]:
                    weighted_rating = turf_rating_data[0]['weighted_rating']
                    turf.ai_rating = weighted_rating
                    turf.save()

                    return Response({'status': "success",
                            'message': "Rating saved",
                            'response_code': status.HTTP_200_OK,
                            'data': serializer.data})
                else:
                    return Response({'status': "error",
                            'message': "Rating unsaved",
                            'response_code': status.HTTP_400_BAD_REQUEST,
                            'data': '{}'})
            else:
                return Response({'status': "error",
                            'message': "Turf not provided",
                            'response_code': status.HTTP_400_BAD_REQUEST,
                            'data': '{}'})
        else:
            return Response({'status': "error",
                        'message': "Not a user",
                        'response_code': status.HTTP_400_BAD_REQUEST,
                        'data': '{}'})
            
               
class RewardPoints(generics.ListAPIView):
    # authentication_classes=[TokenAuthentication]
    permission_classes = [IsUserOnlyReward]
    serializer_class = RewardPointSerializer
    
    def get_queryset(self):
        # pk = self.kwargs['pk']
        pk =self.request.user.pk
        return RewardPointModel.objects.filter(user=pk)
    
    def list(self,request , *args, **kwargs):
        # user = self.kwargs['pk']
        user =self.request.user.pk
        # print("permission",self.permission_classes)
        reward_points = RewardPointModel.objects.filter(user=user).aggregate(total_points=models.Sum('reward_points'))
        
        if not reward_points['total_points']:
            total_points = 0
        else:
            total_points = reward_points['total_points']
            
        response_data = {
            'user': user,
            'total_points': total_points,
            'reward_points': self.serializer_class(self.get_queryset(), many=True).data
        }

        return Response({'status': "success",
                        'message': "listed successfully",
                        'response_code': status.HTTP_200_OK,
                        'data': response_data})
    
    
    
class UserBookingHistoryView(generics.ListAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsUserOnlyBookingHistory]
    serializer_class = UserBookingHistorySerializer

    def get_queryset(self):
        user = self.request.user
        pk = Customer.objects.get(customer=user)
        # print("pk ",pk)
        return UserBookingHistory.objects.filter(user=pk)

    
class RedeemRewards(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUserOnlyHistory]
    serializer_class = RedeemRewardsSerializer

    def get_queryset(self):
        logged_user = self.request.user
        if logged_user.usertype == "customer":
            try:
                user = Customer.objects.get(customer=logged_user)
                return RedeemRewardsModel.objects.filter(user=user)
            except Customer.DoesNotExist:
                return RedeemRewardsModel.objects.none()
        else:
            raise PermissionDenied(detail="Logged user is not a customer.")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        logged_user = self.request.user
        if logged_user.usertype == "customer":
            try:
                user = Customer.objects.get(customer=logged_user)
            except Customer.DoesNotExist:
                return Response({'status': "failed", 'message': 'User not found', 'response_code': status.HTTP_404_NOT_FOUND})

            reward = serializer.validated_data.get('reward') 

            if not reward or user.reward_points < reward.reward_points:
                return Response({'status': "failed", 'message': 'Not enough reward points or invalid reward', 'response_code': status.HTTP_422_UNPROCESSABLE_ENTITY})

            instance = serializer.save(redeemed_date=timezone.now())

            user.reward_points -= reward.reward_points
            user.save()
            instance = serializer.save(user=user)

            response_data = {
                'user': user.customer.username,
                'redeemed_reward': reward.reward_name,
                'redeemed_date': instance.redeemed_date if instance else None,
                'remaining_points': user.reward_points,
            }

            return Response({'status': "success", 'message': "Reward redeemed successfully", 'response_code': status.HTTP_201_CREATED, "data": response_data})
        
        else:
            raise PermissionDenied(detail="Logged user is not a customer.")
        
        
        
class TurfBookedHistory(generics.ListAPIView):
    serializer_class = TurfBookingSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return TurfBooking.objects.filter(turf=pk)