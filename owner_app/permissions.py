from rest_framework import permissions
from rest_framework import exceptions
from owner_app.models import *

class IsOwnerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            if user.usertype == "owner":
                return True
            else:
                response_data = {"status": "failed", "reason": "You are not the owner"}
                raise exceptions.PermissionDenied(response_data)
        else:
            response_data = {"status": "failed", "reason": "Authentication credentials were not provided"}
            raise exceptions.AuthenticationFailed(response_data)
            
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated and user.usertype == "owner":
            if obj.owner.abstract.username == user.username:
                return True
            else:
                response_data = {"status": "failed", "reason": "You are not the owner of this turf"}
                raise exceptions.PermissionDenied(response_data)
        else:
            response_data = {"status": "failed", "reason": "Authentication credentials were not provided or you are not an owner"}
            raise exceptions.AuthenticationFailed(response_data)
        
class IsUserOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        
        if user.is_authenticated:
            if user.usertype == "customer":
                if not RewardPointModel.objects.filter(user__customer__username=user.username).exists():
                    return True
                else:
                    response_data = {"status": "failed", "reason": "Unauthorized user"}
                    raise exceptions.PermissionDenied(response_data)
            else:
                response_data = {"status": "failed", "reason": "You are not a customer"}
                raise exceptions.PermissionDenied(response_data)
        
        
class IsUserOnlyReward(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        # print("IsUser", user)
        if request.method == "GET" or "POST":
            if user.is_authenticated and user.usertype == "customer":
                # print("entering customer")
                if request.method == "POST" or request.method == "GET":
                    if not RewardPointModel.objects.filter(user__customer__username=user.username).exists():
                        # print("Found customer")
                        return True
                    else:
                        response_data = {"status": "failed", "reason": "Unauthorized user"}
                        raise exceptions.PermissionDenied(response_data)
            else:
                response_data = {"status": "failed", "reason": "You are not a customer"}
                raise exceptions.PermissionDenied(response_data)

class CustomerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        
        if user.is_authenticated:
            if user.usertype == "customer":
                return True
            else:
                response_data = {"status": "failed", "reason": "You are not customer"}
                raise exceptions.PermissionDenied(response_data)
        else:
            response_data = {"status": "failed", "reason": "Unauthorized user"}
            raise exceptions.PermissionDenied(response_data)


    # def has_object_permission(self, request, view, obj):
    #     user = request.user

    #     if user.is_authenticated and user.usertype == "customer":
    #         if RewardPointModel.objects.filter(user__customer__username=user.username):
    #             return True
    #         else:
    #             response_data = {"status": "failed", "reason": "You are not the owner of this turf"}
    #             raise exceptions.PermissionDenied(response_data)
    #     else:
    #         response_data = {"status": "failed", "reason": "You are not a customer"}
    #         raise exceptions.PermissionDenied(response_data)
            
            
            
class IsUserOnlyHistory(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        print("IsUser", user)

        if request.method == "GET" or "POST":
            if user.is_authenticated and user.usertype == "customer":
                # print("entering customer")
                # print("user username",user.username)
                # if UserBookingHistory.objects.filter(user__customer_name=user.username).exists():
                #     print("Found customer")
                #     return True
                if not RedeemRewardsModel.objects.filter(user__customer__username=user.username).exists():
                    # print("Found customer RedeemRewardsModel")
                    return True
                elif RedeemRewardsModel.objects.filter(user__customer__username=user.username).exists():
                    return True
                
                else:
                    response_data = {"status": "failed", "reason": "Unauthorized user"}
                    raise exceptions.PermissionDenied(response_data)
            else:
                response_data = {"status": "failed", "reason": "You are not a customer"}
                raise exceptions.PermissionDenied(response_data)
            
            
            