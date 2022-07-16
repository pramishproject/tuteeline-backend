from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound, APIException

class StudentUserNotFound(NotFound):
    default_detail = _('Student user   not  found for following email.')