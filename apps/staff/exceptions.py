from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound


class StaffNotFound(NotFound):
    default_detail = _('Staff not  found for following Id.')
