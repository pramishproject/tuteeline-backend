from rest_framework.permissions import BasePermission


class IsNormalUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user.is_authenticated and not user.is_staff)

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj)

