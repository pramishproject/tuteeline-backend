from rest_framework import serializers

from apps.consultancy_course.models import ConsultancyCourse


class ListConsultancyCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultancyCourse
        fields = (
            'course',
            'fee',
            'currency',
            'course_description',
        )