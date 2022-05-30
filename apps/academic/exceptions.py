from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound, APIException


class AcademicNotFound(NotFound):
    default_detail = _('student academic not  found for following Id.')

class SopNotFound(NotFound):
    default_detail = _('student sop not  found for following Id.')

class LorNotFound(NotFound):
    default_detail = _('student lor not  found for following Id.')

class EssayNotFound(NotFound):
    default_detail = _('student essay not  found for following Id.')