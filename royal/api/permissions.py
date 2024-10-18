from rest_framework.permissions import BasePermission

class IsAdminOrSuperuser(BasePermission):
    """
    Custom permission to only allow admin users or superusers to access the view.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_admin or request.user.is_superuser)


class IsAdmin(BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

class IsSuperuser(BasePermission):
    """
    Custom permission to only allow superusers to access the view.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser
