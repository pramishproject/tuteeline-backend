from apps.core.usecases import BaseUseCase
from apps.linkage.models import Linkage


class CreateLinkageUseCase(BaseUseCase):
    def __init__(self,consultancy,serializer):
        self._consultancy = consultancy
        self._serializer = serializer
        self._data = self._serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        # todo add document too
        Linkage.objects.create(
            consultancy=self._consultancy,
            **self._data
        )

class ListInstituteLinkageConsultancyUseCase(BaseUseCase):
    def execute(self):
        self._factory()
        return self._linkage

    def _factory(self):
        self._linkage = Linkage.objects.all()
