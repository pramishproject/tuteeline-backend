from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound


class SettingsNotFound(NotFound):
    default_detail = _('Setting not  found for given query.')
