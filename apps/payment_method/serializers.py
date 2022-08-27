from rest_framework import serializers

from apps.payment_method.models import Provider, VoucherPayment


class AddProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = (
            'provider_id',
            'name',
        )

class ListProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'

class AddVoucherPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherPayment
        fields = (
            'account_no',
            'branch',
            'account_name',
            'bank_name',
        )

class ListVoucherPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherPayment
        fields = '__all__'