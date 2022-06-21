from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound, APIException,ValidationError


class AlreadyBooked(APIException):
    default_detail = _('already booked for this time')

class TimeError(APIException):
    default_detail = _("counselling time is grater then today time")