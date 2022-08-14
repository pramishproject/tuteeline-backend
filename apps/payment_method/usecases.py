from apps.core.usecases import BaseUseCase
from apps.payment_method.models import Provider


class AddProviderUseCase(BaseUseCase):
    def __init__(self,serializer,institute):
        self._institute = institute
        self._serializer = serializer.validated_data

    def execute(self):
        self._factory()
    def _factory(self):
        Provider.objects.create(
                    **self._serializer,
                    institute=self._institute
                )