from apps.core.usecases import BaseUseCase
from apps.institute.exceptions import InstituteNotFound
from apps.institute.models import Institute
from apps.review.exceptions import ReviewNotFound
from apps.review.models import InstituteReview
from django.utils import timezone

class CreateInstituteReviewUseCase(BaseUseCase):
    def __init__(self,student,serializer):
        self._student = student
        self._serializer = serializer
        self._data = self._serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):

        InstituteReview.objects.create(
            student= self._student,
             **self._data,
        )

class GetInstituteReviewByIdUseCase(BaseUseCase):
    def __init__(self,institute_review_id):
        self._institute_review_id = institute_review_id

    def execute(self):
        self._factory()
        return self._institute_review

    def _factory(self):
        try:
            self._institute_review=InstituteReview.objects.get(pk=self._institute_review_id)
        except InstituteReview.DoesNotExist:
            raise ReviewNotFound
        

class UpdateInstituteReviewUseCase(BaseUseCase):
    def __init__(self,review,serializer):
        self._review = review
        self._serializer = serializer
        self._data = self._serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        for data in self._data.keys():
            setattr(self._review, data, self._data[data])
        self._review.updated_at = timezone.now()
        self._review.save()


class ListInstituteReviewUseCase(BaseUseCase):
    def __init__(self,institute):
        self._institute =institute
    def execute(self):
        self._factory()
        return self._review

    def _factory(self):
        self._review = InstituteReview.objects.filter(institute= self._institute)