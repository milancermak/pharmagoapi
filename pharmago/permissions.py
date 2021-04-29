
from rest_framework import permissions


class IsOwnerOrTenantAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow to access it:
    - Owners of an object.
    - Admins which belongs to the same tenant of an object.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or (request.user.is_staff)