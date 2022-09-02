from rest_framework import serializers

from apps.payment_method.models import Provider, VoucherPayment, ProviderName,Transaction


class AddProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = (
            'provider',
            'receiver',
        )

class ListProviderNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderName
        fields = "__all__"

class ListProviderSerializer(serializers.ModelSerializer):
    name = serializers.DictField(source="get_provider_name")
    class Meta:
        model = Provider
        fields = (
            'id',
            'institute',
            'receiver',
            'provider',
            'name',
            'created_at',
            'updated_at',
        )

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

class TransactionSerializer(serializers.ModelSerializer):
    approve_by = serializers.UUIDField()
    class Meta:
        model = Transaction
        fields = (
            'payment_method',
            'payment_type',
            'approve_by',
        )