from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound


class PortalNotFound(NotFound):
    default_detail = _('Portal not  found for following Id.')
