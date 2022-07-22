from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _

class UniqueKeyError(APIException):
    status_code = 409
    default_detail = _("already exist to this university")
    default_code = 'service_unavailable'

class UniversityIsNotAffiliated(APIException):
    status_code = 409
    default_detail = _("you are not university")
    default_code = 'service_unavailable'

class CollegeIsNotAffiliated(APIException):
    status_code = 409
    default_detail = _("you are not college")
    default_code = 'service_unavailable'

class MultipleUniversityError(APIException):
    status_code = 409
    default_detail = _("Multiple university for same course")
    default_code = 'service_unavailable'

class TypeValidationError(APIException):
    status_code = 409
    default_detail = _("type field is mission")
    default_code = 'service_unavailable'