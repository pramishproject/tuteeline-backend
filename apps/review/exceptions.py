from rest_framework.exceptions import NotFound, APIException
from django.utils.translation import gettext_lazy as _

class ReviewNotFound(NotFound):
    default_detail = _('Review not  found for following Id.')

class ReviewAlreadyExist(APIException):
    status_code = 409
    default_detail = _("Review is already Exist")