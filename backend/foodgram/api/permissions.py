from rest_framework import permissions


class CustomReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
        )


class IsUserReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in ['GET']
