from .serializers  import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

# Create your views here.


class Registration(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    
    def post(self,request):
        data = {}
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            token, create = Token.objects.get_or_create(user=account)
            token_key = token.key
            print('token ', token)
            data ={
                "message":"Account Created Successfully",
                "Organization_name":account.Organization_name,
                "username":account.username,
                "email":account.email,
                "Phone_number":account.Phone_number,
                "token":token_key
            }   
        else:
            data = serializer.errors
        
        return Response(data)
    
    
    
class TurfCreate(generics.CreateAPIView, generics.ListAPIView):
    queryset = Turf.objects.all()
    serializer_class = TurfSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            d = serializer.save()
            data = {
                "message" : "turf created successfully",
                "turf name" : d.name
            }
            return Response(data)
        else:
            return Response(serializer.errors)
        
class TurfManagement(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TurfSerializer
    
    def get_queryset(self):
        id = self.kwargs['id']
        return Turf.objects.filter(id=id)
    