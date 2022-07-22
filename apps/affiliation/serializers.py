from rest_framework import serializers

from apps.affiliation.models import Affiliation
from apps.institute.serializers import ListInstituteSerializer


class AddAffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = (
            'university',
            'course',
        )

class ListOfAffiliation(serializers.ModelSerializer):
    institute = ListInstituteSerializer(read_only=True,many=False)
    university = ListInstituteSerializer(read_only=True,many=False)
    class Meta:
        model = Affiliation
        fields = (
            'institute',
            'university',
            'course',
        )