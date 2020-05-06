from rest_framework import permissions


class IsAuthenticatedSuperuser(permissions.BasePermission):
# Default permissions class to check if the user is a superuser 
# before giving access to the unsafe methods in the request 
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True 
        return request.user.is_superuser