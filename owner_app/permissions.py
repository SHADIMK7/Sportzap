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