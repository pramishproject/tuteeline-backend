from rest_framework import serializers

from apps.affiliation.models import Affiliation


class AddAffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = (
            'university',
            'course',
        )