from apps.core.usecases import BaseUseCase
from apps.payment_method.models import Provider, VoucherPayment, ProviderName, Receiver
from django.utils.datetime_safe import datetime
import requests as req

class GetProviderUseCase(BaseUseCase):
    def __init__(self,provider_payment_id):
        self._provider_id = provider_payment_id

    def execute(self):
        self._factory()
        return self._provider

    def _factory(self):
        self._provider = Provider.objects.get(pk = self._provider_id)

class GetVoucherUseCase(BaseUseCase):
    def __init__(self,voucher_id):
        self._voucher_id = voucher_id

    def execute(self):
        self._factory()
        return self._voucher

    def _factory(self):
        self._voucher = VoucherPayment.objects.get(pk = self._voucher_id)

class AddProviderUseCase(BaseUseCase):
    def __init__(self,serializer,institute):
        self._institute = institute
        self._serializer = serializer
        self._data = self._serializer.validated_data

    def execute(self):
        self._factory()
    def _factory(self):
        receiver_id = self._data.get("receiver_id")
        receiver = Receiver.objects.create(
            receiver_id=receiver_id
        )
        Provider.objects.create(
                    provider=self._data.get("provider"),
                    receiver=receiver,
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

class DeleteProviderUseCase(BaseUseCase):
    def __init__(self,provider:Provider):
        self._provider = provider

    def execute(self):
        self._provider.delete()

class DeleteVoucherUseCase(BaseUseCase):
    def __init__(self,voucher:VoucherPayment):
        self._voucher = voucher

    def execute(self):
        self._voucher.delete()

class EsewaVerifyUseCase(BaseUseCase):
    def __init__(self,apply):
        self._apply = apply
    def execute(self):
        self._factory()
    def _factory(self):
        url = "https://uat.esewa.com.np/epay/main"
        apply = self.get_object()
        fee = apply.course.reg_fee
        d = {'amt': fee,
             'pdc': 0,
             'psc': 0,
             'txAmt': 0,
             'tAmt': 100,
             'pid': apply.id,
             'scd': 'EPAYTEST',
             'su': 'http://merchant.com.np/page/esewa_payment_success?q=su',
             'fu': 'http://merchant.com.np/page/esewa_payment_failed?q=fu'}
        resp = req.post(url, d)