from rest_framework import serializers

from apps.college.models import College


class CollegeSearchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['id', 'name']
