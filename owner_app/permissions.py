from rest_framework import permissions
from rest_framework import exceptions

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