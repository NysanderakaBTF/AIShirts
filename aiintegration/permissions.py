from rest_framework import permissions


class CanDeleteImagePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated and obj.prompt.owner == request.user) or request.user.is_staff


class CanViewAIparams(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff
