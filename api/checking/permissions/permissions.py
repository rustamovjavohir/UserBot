from rest_framework.permissions import BasePermission

from apps.staff.models import Workers
from config.settings import ALLOWED_IPS


class RadiusPermission(BasePermission):
    def has_permission(self, request, view):
        if request.META.get('HTTP_NAME') == 'Radius':
            return True
        return False


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        worker = request.user.workers_set.first()
        if worker:
            return True if worker.is_boss or worker.role in [Workers.Role.ADMIN, Workers.Role.SUPER_ADMIN] else False
        return False


class SuperAdminPermission(BasePermission):
    def has_permission(self, request, view):
        worker = request.user.workers_set.first()
        if worker:
            return True if worker.role == Workers.Role.SUPER_ADMIN else False
        return False


class AllowIPPermission(BasePermission):
    def has_permission(self, request, view):
        ip = request.META.get('REMOTE_ADDR')
        print(ip)
        print("allow: ", ALLOWED_IPS)
        if ip in ALLOWED_IPS:
            return True
        return True
