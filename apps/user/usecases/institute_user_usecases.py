from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound

from apps.core.usecases import BaseUseCase
from apps.user.models import InstituteUser


class InstituteUserNotFound(NotFound):
    default_detail = _('Portal User Not Found for following Id.')


class GetInstituteUserUseCase(BaseUseCase):
    def __init__(self, institute_user_id):
        self._institute_user_id = institute_user_id

    def execute(self):
        self._factory()

        return self._user

    def _factory(self):
        try:
            self._user = InstituteUser.objects.get(pk=self._institute_user_id)
            
        except InstituteUser.DoesNotExist:
            raise InstituteUserNotFound
