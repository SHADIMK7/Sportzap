from django.shortcuts import get_object_or_404
from .serializers  import *
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from user_app.models import *
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
from django.views import View
from django.shortcuts import render, redirect
from user_app.help import generate_random_password
from django.conf import settings




# Create your views here.




class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Both username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)

            if user.is_superuser:
                user_id = user.id
            elif user.usertype == 'owner':
                owner_id = Owner.objects.get(abstract=user)
                user_id = owner_id.id
            elif user.usertype == 'customer':
                customer_id = Customer.objects.get(customer=user)
                user_id = customer_id.id
            elif user.is_staff:
                user_id = 1
            else:
                user_id = None

            user_type = user.usertype

            response_data = {
                'token': token.key,
                'user_type': user_type,
                'is_admin': user.is_superuser,
                'user_id': user_id
            }
            # print("user id is ", user_id)

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

class ResetPass(APIView):
    serializer_class = ResetPasswordSerializer 

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        user = Abstract.objects.filter(email=email).first()

        if user:
            new_pass = generate_random_password()
            user.set_password(new_pass)
            user.save()

            message = render_to_string('reset_pass.html', {'new_pass': new_pass, 'email': email})
            plain_message = strip_tags(message)

            subject = 'Sportzap Reset password'
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
                'response_code': status.HTTP_201_CREATED,
                'message': "Password reset successful. New password has been sent to your email",
            })
        else:
            return Response({
                "status": "failed",
                "response code": status.HTTP_400_BAD_REQUEST,
                "message": "No such email registered"
            })


class Registration(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        data = {}
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            token, create = Token.objects.get_or_create(user=account.abstract)
            token_key = token.key
            data = {
                "message": "Account Created Successfully",
                "Organization_name": account.Organization_name,
                "username": account.abstract.username,
                "email": account.abstract.email,
                "Phone number": account.abstract.phone_no,
                "token": token_key
            }
            return Response({'status':"success",'response_code': status.HTTP_201_CREATED,'data': data,})
        else:
            data = serializer.errors

        return Response(data)
    


    

    
class TurfCreate(generics.CreateAPIView, generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOnly]
    # queryset = Turf.objects.all()
    serializer_class = TurfSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Turf.objects.filter(owner__pk=pk)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        serializer = self.serializer_class(data=request.data, context={'owner_pk': pk})
        if serializer.is_valid():
            d = serializer.save()
            response = TurfSerializer(d)
            return Response({'status': "success", 'message': response.data, 'response_code': status.HTTP_201_CREATED})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class TurfDisplay(generics.ListAPIView):
    serializer_class = TurfSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Turf.objects.filter(pk=pk)


class TurfDisplayAll(generics.ListAPIView):
    serializer_class = TurfSerializer
    queryset = Turf.objects.all()
        
class TurfManagement(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOnly]
    
    serializer_class = TurfSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Turf.objects.filter(pk=pk)
    
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        response = TurfSerializer(instance)

        # updated_data = {
        #     'owner': instance.owner,
        #     'name': serializer.validated_data.get('name', instance.name),
        #     'location': serializer.validated_data.get('location', instance.location),
        #     'price': serializer.validated_data.get('price', instance.price),
        #     'image': serializer.validated_data.get('image', instance.image),
        #     'description': serializer.validated_data.get('description', instance.description),
        #     'amenity': [amenity.name for amenity in serializer.validated_data.get('amenity', instance.amenity.all())],
        #     'latitude': serializer.validated_data.get('latitude', instance.latitude),
        #     'longitude': serializer.validated_data.get('longitude', instance.longitude),
        # }

        return Response({
            'status': "success",
            'message': "Turf updated successfully",
            'response_code': status.HTTP_200_OK,
            'data': response.data,
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object() 
        self.perform_destroy(instance)
        return Response({'status':"success",'message': "Turf deleted successfully",'response_code': status.HTTP_200_OK,})


# class TurfPriceUpdate(generics.ListAPIView):
#     serializer_class = TurfPriceUpdateSerializer

#     def get_queryset(self):
#         pk = self.kwargs['pk']
#         return TurfPriceUpdateModel.objects.filter(turf__owner=pk)

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = TurfPriceUpdateSerializer(queryset, context={'owner_id': self.kwargs['pk']}, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class PaymentHistory(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOnly]
    serializer_class = PaymentHistorySerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.usertype == "owner":
            return PaymentHistoryModel.objects.filter(turf__owner__abstract__username=user.username)
        else:
            return PaymentHistoryModel.objects.none()
        

class MatchRating(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOnly]
    serializer_class = MatchRatingSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        owner = self.request.user.owner_set.first()
        
        if owner and owner.pk == int(pk):
            return MatchRatingModel.objects.filter(turf__owner=pk)
        else:
            response_data = {
                'status': "failed",
                'reason': "You are not the owner of this turf",
                'response_code': status.HTTP_403_FORBIDDEN,
            }
            raise PermissionDenied(response_data)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        
        owner = request.user.owner_set.first() 
        if not owner or owner.pk != int(pk):
            response_data = {
                'status': "failed",
                'reason': "You are not the owner of this turf",
                'response_code': status.HTTP_403_FORBIDDEN,
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=request.data, context={'owner_pk': pk})
        
        if serializer.is_valid():
            content = serializer.save()
            
            response_data = {
                'status': "success",
                'message': "Match has been rated successfully",
                'response_code': status.HTTP_201_CREATED,
                'data': serializer.data,
            }
            
            return Response({'status':"success",'message': "Match rated successfully",'response_code': status.HTTP_201_CREATED,"data":response_data})
        else:
            return Response({'status': "failed",'message': "Serializer is not valid",'response_code':status.HTTP_400_BAD_REQUEST})
    
    
# class PaymentHistory(generics.ListCreateAPIView):
#     queryset = PaymentHistory.objects.all()
#     serializer_class = PaymentHistorySerializer

# class PaymentHistoryDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = PaymentHistory.objects.all()
#     serializer_class = PaymentHistorySerializer

# class UpdatePaymentHistoryView(generics.UpdateAPIView):
#     def put(self, request, booking_id, *args, **kwargs):
#         booking = get_object_or_404(TurfBooking, pk=booking_id)
        
#         if booking.has_expired():
#             PaymentHistory.objects.create(user=booking.user, amount=booking.price)
#             return Response({'message': 'Payment added to history.'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'message': 'Booking has not expired yet.'}, status=status.HTTP_400_BAD_REQUEST)



class AmenityView(generics.ListAPIView):
    serializer_class = AmenitySerializer
    queryset = Amenity.objects.all()
    

    
class OwnerDelete(generics.DestroyAPIView):
    
    def delete(self, request, *args, **kwargs):
        user = self.request.user

        owner = user
        if owner:
            owner.delete()
            return Response({'status': 'success'})
        else:
            return Response({'status': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
class ChangePasswordOwner(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOnly]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.check_password(serializer.validated_data['old_password']):
                request.user.set_password(serializer.validated_data['new_password'])
                request.user.save()
                return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)