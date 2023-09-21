from rest_framework import permissions


class CustomReadOnly(permissions.BasePermission):
    """Разрешение админа или только чтение."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
        )
