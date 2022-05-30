from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound

from apps.core.usecases import BaseUseCase
from apps.user.models import ConsultancyUser


class ConsultancyUserNotFound(NotFound):
    default_detail = _('User Not Found for following Id.')


class GetConsultancyUserUseCase(BaseUseCase):
    def __init__(self, consultancy_user_id):
        self._consultancy_user_id = consultancy_user_id

    def execute(self):
        self._factory()
        return self._user

    def _factory(self):
        try:
            self._user = ConsultancyUser.objects.get(pk=self._consultancy_user_id)
        except ConsultancyUser.DoesNotExist:
            raise ConsultancyUserNotFound
