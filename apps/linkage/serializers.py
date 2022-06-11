from rest_framework import serializers

from apps.linkage.models import Linkage


class InstituteLinkageListSerializer(serializers.ModelSerializer):
    constantly_data = serializers.DictField(source='get_consultancy_data')
    class Meta:
        model = Linkage
        fields = (
            'institute',
            'consultancy',
            'constantly_data'
        )