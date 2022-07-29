from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound,APIException


class StaffNotFound(NotFound):
    default_detail = _('Staff not  found for following Id.')

class PermissionFormatError(APIException):
    default_detail = _('should be list')

class UnKnownPermissionType(APIException):
    default_detail = _('unknown permission list')