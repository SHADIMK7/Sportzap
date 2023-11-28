from .serializers  import *
from rest_framework import generics
from rest_framework.response import Response
# Create your views here.

class Registration(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    
    def post(self,request):
        data = {}
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            data ={
                "message":"Account Created Successfully",
                "Organization_name":account.Organization_name,
                "first_name":account.first_name,
                "last_name":account.last_name,
                "email":account.email,
                "Phone_number":account.Phone_number
            }   
        else:
            data = serializer.errors
        
        return Response(data)
    
    
    
class TurfView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Turf.objects.all()
    serializer_class = TurfSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            d = serializer.save()
            data = {
                "message" : "turf created successfully",
                "turf name" : d.turf_name
            }
            return Response(data)
        else:
            return Response(serializer.errors)