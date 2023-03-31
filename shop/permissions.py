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