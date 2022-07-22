from apps.affiliation.models import Affiliation
from apps.core.usecases import BaseUseCase
from apps.affiliation.exceptions import UniqueKeyError
from django.db import IntegrityError
class AddAffiliationUseCase(BaseUseCase):
    def __init__(self,institute,serializer):
        self._institute = institute
        self._data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        try:
            Affiliation.objects.create(
                institute = self._institute,
                **self._data,
            )
        except IntegrityError:
            raise UniqueKeyError
