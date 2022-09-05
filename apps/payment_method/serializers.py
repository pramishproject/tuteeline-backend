from rest_framework import serializers

from apps.payment_method.models import Provider, VoucherPayment, ProviderName,Transaction


class AddProviderSerializer(serializers.ModelSerializer):
    receiver_id = serializers.CharField(max_length=200)
    class Meta:
        model = Provider
        fields = (
            'provider',
            'receiver_id',
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
    voucher_id = serializers.UUIDField(required=False)
    class Meta:
        model = Transaction
        fields = (
            'payment_method',
            'payment_type',
            'approve_by',
            'voucher_id',
        )