from owner_app .models import *
from rest_framework.response import Response
from rest_framework import status


def check_mobile(mobile):
    if Abstract.objects.filter(phone_no = mobile).first():
        return Response({'status': "failed",
                            'message': "Mobile number already exists",
                            'response_code':status.HTTP_400_BAD_REQUEST})
    else:
        return None
    
def check_email(email):
    if Abstract.objects.filter(email = email).first():
        return Response({'status': "failed",
                             'message': "Email already exists",
                             'response_code':status.HTTP_400_BAD_REQUEST})
    else:
        return None
            