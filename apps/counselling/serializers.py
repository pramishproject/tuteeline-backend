from rest_framework import serializers
from apps.counselling import models

class CreateInstituteCounsellingSerializer(serializers.ModelSerializer):
    interested_courses = serializers.CharField(allow_blank=True,required=False)
    class Meta:
        model =  models.InstituteCounselling
        fields = (
            'institute',
            'education_level',
            'which_time',
            'physical_counelling',
            'interested_courses',
        )

