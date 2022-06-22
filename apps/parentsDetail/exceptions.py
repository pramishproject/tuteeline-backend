from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound, APIException
from django.db import IntegrityError

class ParentsNotFound(NotFound):
    default_detail = _('Parents not  found for following Id.')

class UniqueKeyError(APIException):
    status_code = 409
    default_detail = _("parents relation should be unique")
    default_code = 'service_unavailable'