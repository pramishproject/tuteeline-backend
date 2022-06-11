from apps.core.usecases import BaseUseCase
from apps.linkage.models import Linkage


class ListInstituteLinkageConsultancyUseCase(BaseUseCase):
    def execute(self):
        self._factory()
        return self._linkage

    def _factory(self):
        self._linkage = Linkage.objects.all()
