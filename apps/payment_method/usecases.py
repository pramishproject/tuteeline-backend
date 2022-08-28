from apps.core.usecases import BaseUseCase
from apps.payment_method.models import Provider, VoucherPayment, ProviderName
from django.utils.datetime_safe import datetime

class GetProviderUseCase(BaseUseCase):
    def __init__(self,provider_payment_id):
        self._provider_id = provider_payment_id

    def execute(self):
        self._factory()
        return self._provider

    def _factory(self):
        self._provider = Provider.objects.get(pk = self._provider_id)

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

class ListProviderNameUseCase(BaseUseCase):
    def execute(self):
        self._factory()
        return self._provider

    def _factory(self):
        self._provider=ProviderName.objects.all()

class ListProviderUseCase(BaseUseCase):
    def __init__(self,institute):
        self._institute = institute

    def execute(self):
        self._factory()
        return self._provider

    def _factory(self):
        self._provider = Provider.objects.filter(institute=self._institute)

class CustomUpdateUseCase(BaseUseCase):
    def __init__(self, instance, serializer):
        self._instance= instance
        self._data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        for key in self._data.keys():
            setattr(self._instance, key, self._data.get(key))

        self._instance.updated_at = datetime.now()
        self._instance.save()

class CreateVoucherPaymentDetail(BaseUseCase):
    def __init__(self,institute,serializer):
        self._institute = institute
        self._data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        VoucherPayment.objects.create(
            **self._data,
            institute=self._institute
        )

class ListVoucherUseCase(BaseUseCase):
    def __init__(self,institute):
        self._institute = institute

    def execute(self):
        self._factory()
        return self._voucher

    def _factory(self):
        self._voucher = VoucherPayment.objects.filter(
            institute=self._institute
        )