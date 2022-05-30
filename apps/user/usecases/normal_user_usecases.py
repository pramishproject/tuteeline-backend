from apps.core import usecases
from apps.user.models import NormalUser


class ListNormalUserUseCase(usecases.BaseUseCase):
    def execute(self):
        return self._factory()

    def _factory(self):
        return NormalUser.objects.select_related(
            'user'
        ).unarchived()

