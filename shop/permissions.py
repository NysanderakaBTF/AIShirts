from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnlyOrStaffOnlyPermission(BasePermission):
    """
    Allows anyone to view objects only but restricts the ability to create, update and delete objects only to staff users
    """

    def has_permission(self, request, view):
        # Allow read-only access for all users.
        if request.method in SAFE_METHODS:
            return True
        # Restrict write access to staff users only.
        return request.user.is_staff


class ModifyOrdersPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in request.SAFE_METHOD:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return True
        return request.user.is_staff


class IsOwnerOrStaffOnly(BasePermission):
    """
    Custom permission to only allow owners of an object or staff members to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the request user is a staff member
        if request.user.is_staff:
            return True

        # Check if the bucket belongs to the request user
        return obj.user == request.user