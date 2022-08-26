from rest_framework import serializers

from apps.payment_method.models import Provider


class AddProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = (
            'provider_id',
            'name',
        )

