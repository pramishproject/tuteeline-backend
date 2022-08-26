from apps.core import generics
from apps.institute.mixins import InstituteMixins
from apps.payment_method import usecases
from apps.payment_method.mixins import ProviderMixins
from apps.payment_method.serializers import AddProviderSerializer


class AddProviderPaymentMethod(generics.CreateAPIView,InstituteMixins):
    serializer_class = AddProviderSerializer
    def get_object(self):
        return self.get_institute()

    def perform_create(self, serializer):
        return usecases.AddProviderUseCase(
            serializer=serializer,
            institute=self.get_object()
        ).execute()

class UpdateProviderPaymentMethod(generics.UpdateWithMessageAPIView,ProviderMixins):
    serializer_class = AddProviderSerializer
    def get_object(self):
        return self.get_provider()

    def perform_update(self, serializer):
        return usecases.CustomUpdateUseCase(
            instance=self.get_object(),
            serializer=serializer
        ).execute()

# class AddVoucherPaymentDetail(generics.A)
