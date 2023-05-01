from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied


class IsRadiusMixin(AccessMixin):
    """ Verify that the current user is Radius user. """

    def dispatch(self, request, *args, **kwargs):
        if request.META.get('HTTP_NAME') == 'Radius' or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied('Permission denied')
