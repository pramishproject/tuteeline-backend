from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound, APIException


class ConsultancyNotFound(NotFound):
    default_detail = _('Consultancy not  found for following Id.')


class ConsultancyStaffNotFound(NotFound):
    default_detail = _('Consultancy staff  not  found for following Id.')


class ConsultancyUserEmailNotFound(APIException):
    default_detail = _('Consultancy user   not  found for following email.')


class PortalUserEmailNotFound(APIException):
    default_detail = _('Portal user   not  found for following email.')


