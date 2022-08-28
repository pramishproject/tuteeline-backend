from rest_framework import serializers

from apps.payment_method.models import Provider, VoucherPayment, ProviderName


class AddProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = (
            'provider_id',
            'provider_name',
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
            'provider_name',
            'provider_id',
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