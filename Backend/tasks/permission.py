from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsProfileOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsActiveUser(BasePermission):
    message = "Only active users can assign tasks."

    def has_permission(self, request, view):
        return request.user.status == 'active'