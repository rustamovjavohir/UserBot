from rest_framework.permissions import BasePermission

from apps.staff.models import Workers


class RadiusPermission(BasePermission):
    def has_permission(self, request, view):
        if request.META.get('HTTP_NAME') == 'Radius':
            return True
        return False


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.workers_set.first().is_boss:
            return True
        return False
