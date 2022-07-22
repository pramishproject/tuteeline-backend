from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _

class UniqueKeyError(APIException):
    status_code = 409
    default_detail = _("already exist to this university")
    default_code = 'service_unavailable'