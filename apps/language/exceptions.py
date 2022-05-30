from rest_framework.exceptions import NotFound, APIException
from django.utils.translation import gettext_lazy as _

class LanguageNotFound(NotFound):
    default_detail = _('Language not  found for following Id.')