from rest_framework import permissions

class IsTargetUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # allow logged in user to view own details
        return obj == request.user
