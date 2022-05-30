from django.db.models import fields
from rest_framework import serializers

from apps.review.models import InstituteReview


class CreateInstituteReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteReview
        fields = (
            "institute",
            "review",
            "rating",
        )

class UpdateInstituteReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteReview
        fields = (
            "review",
            "rating",
        )

class ListInstituteReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteReview
        fields = '__all__'