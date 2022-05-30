from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound, APIException


class CitizenshipNotFound(NotFound):
    default_detail = _('Citizenship not  found for following Id.')

class PassportNotFound(NotFound):
    default_detail = _('Citizenship not  found for following Id.')