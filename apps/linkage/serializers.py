from rest_framework import serializers

from apps.institute.serializers import ListInstituteSerializer
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

class LinkageInstituteListSerializer(serializers.ModelSerializer):
    institute = ListInstituteSerializer(many=False,read_only=True)
    class Meta:
        model = Linkage
        fields = (
            'institute',
        )