from apps.core import generics
from apps.institute.mixins import InstituteMixins
from apps.institute_course.mixins import CourseMixin, ApplyMixin
from apps.institute_course.models import InstituteCourse
from apps.payment_method import usecases
from apps.payment_method.mixins import ProviderMixins, VoucherMixins
from apps.payment_method.serializers import AddProviderSerializer, AddVoucherPaymentSerializer, ListProviderSerializer, \
    ListVoucherPaymentSerializer, ListProviderNameSerializer
from rest_framework.views import APIView

class ListProviderName(generics.ListAPIView):
    serializer_class = ListProviderNameSerializer
    def get_queryset(self):
        return usecases.ListProviderNameUseCase().execute()

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

class DeleteProviderPaymentMethod(generics.DestroyWithMessageAPIView,ProviderMixins):
    def get_object(self):
        return self.get_provider()

    def perform_destroy(self, instance):
        return usecases.DeleteProviderUseCase(
            provider=self.get_provider()
        ).execute()

class DeleteVoucherPaymentMethod(generics.DestroyWithMessageAPIView,VoucherMixins):
    def get_object(self):
        return self.get_voucher()

    def perform_destroy(self, instance):
        return usecases.DeleteVoucherUseCase(
            voucher=self.get_object()
        ).execute()

class UpdateVoucherPaymentMethod(generics.UpdateWithMessageAPIView,VoucherMixins):
    serializer_class = AddVoucherPaymentSerializer
    def get_object(self):
        return self.get_voucher()

    def perform_update(self, serializer):
        return usecases.CustomUpdateUseCase(
            instance=self.get_object(),
            serializer=serializer,
        ).execute()

class AddVoucherPaymentDetail(generics.CreateWithMessageAPIView,InstituteMixins):
    serializer_class = AddVoucherPaymentSerializer
    def get_object(self):
        return self.get_institute()

    def perform_create(self, serializer):
        return usecases.CreateVoucherPaymentDetail(
            institute=self.get_object(),
            serializer = serializer,
        ).execute()

class ListProviderPaymentMethod(generics.ListAPIView,InstituteMixins):
    serializer_class = ListProviderSerializer
    def get_object(self):
        return self.get_institute()

    def get_queryset(self):
        return usecases.ListProviderUseCase(
            institute=self.get_object(),
        ).execute()

class ListVoucherPaymentView(generics.ListAPIView,InstituteMixins):
    serializer_class = ListVoucherPaymentSerializer
    def get_object(self):
        return self.get_institute()

    def get_queryset(self):
        return usecases.ListVoucherUseCase(
            institute=self.get_object()
        ).execute()


class EsewaVerifyView(generics.CreateAPIView,ApplyMixin):
    def get_object(self):
        return self.get_apply()
    def perform_create(self):
        return usecases.EsewaVerifyUseCase(
            apply=self.get_object()
        ).execute()
