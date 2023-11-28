from django.shortcuts import render
from rest_framework.response import Response
from owner_app.models import Owner
from owner_app.serializers import RegistrationSerializer
from rest_framework.views import APIView
from rest_framework import status


# Create your views here.
class TurfList(APIView):
    def get(self,request):
        turf= Owner.objects.filter(is_staff=False)
        serializer= RegistrationSerializer(turf,many=True,context={'request': request})
        return Response(serializer.data)
    def delete(self,request,pk):
        try:
            stream=Owner.objects.get(pk=pk)
            stream.delete()
            return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Owner.DoesNotExist:
            return Response({"message": "Object does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
# class AdminView(APIView):
#     def get(self,request):


 