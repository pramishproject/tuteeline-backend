from rest_framework import serializers

from apps.review.models import InstituteReview, ConsultancyReview


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
    is_review = serializers.SerializerMethodField()
    def get_is_review(self, obj):
        student_id = self.context['request'].GET.get('student_id', None)
        if student_id != None:
            if str(obj.student.pk) == student_id:
                return True
        return False

    class Meta:
        model = InstituteReview
        fields = (
            'id',
            'rating',
            'review',
            'institute',
            'student',
            'created_at',
            'updated_at',
            'is_review'
        )


class InstituteAggregateReviewSerializer(serializers.Serializer):
    rating = serializers.FloatField()
    rating_count = serializers.IntegerField()



# -----------------consultancy review ----------

class CreateConsultancyReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultancyReview
        fields = (
            "consultancy",
            "review",
            "rating",
        )

class ListConsultancyReviewSerializer(serializers.ModelSerializer):
    is_review = serializers.SerializerMethodField()
    def get_is_review(self, obj):
        student_id = self.context['request'].GET.get('student_id', None)
        if student_id != None:
            if str(obj.student.pk) == student_id:
                return True
        return False

    class Meta:
        model = ConsultancyReview
        fields = (
            'id',
            'rating',
            'review',
            'consultancy',
            'student',
            'created_at',
            'updated_at',
            'is_review'
        )

class UpdateConsultancyReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultancyReview
        fields = (
            'rating',
            'review',
        )