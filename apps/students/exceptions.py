from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound, APIException
from django.db import IntegrityError



class StudentModelNotFound(NotFound):
    default_detail = _('Student Not Found for following Id')


class StudentAddressUnique(IntegrityError):
    default_detail = _('address already exist')

class FavouriteInstituteNotFound(NotFound):
    default_detail = _('this id doesnt exist exist')