from django.db.models import Count

from apps.core.usecases import BaseUseCase
from apps.institute.exceptions import InstituteNotFound
from apps.institute.models import Institute
from apps.review.exceptions import ReviewNotFound, ReviewAlreadyExist
from apps.review.models import InstituteReview, ConsultancyReview
from django.utils import timezone

class CreateInstituteReviewUseCase(BaseUseCase):
    def __init__(self,student,serializer):
        self._student = student
        self._serializer = serializer
        self._data = self._serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        try:
            InstituteReview.objects.create(
                student= self._student,
                 **self._data,
            )
        except Exception as e:
            raise ReviewAlreadyExist

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


class GetAggregateInstituteReviewUseCase(BaseUseCase):
    def __init__(self,institute):
        self._institute = institute

    def execute(self):
        self._factory()
        return self.review

    def _factory(self):
        # pass
        self.review = list(InstituteReview.objects.filter(institute=self._institute).values("rating").\
            annotate(rating_count=Count("rating")))

# ------------------------------consultancy --------

class GetConsultancyReviewByIdUseCase(BaseUseCase):
    def __init__(self,consultancy_review_id):
        self._consultancy_review_id = consultancy_review_id

    def execute(self):
        self._factory()
        return self._consultancy_review

    def _factory(self):
        try:
            self._consultancy_review=ConsultancyReview.objects.get(pk=self._consultancy_review_id)
        except ConsultancyReview.DoesNotExist:
            raise ReviewNotFound

class GetAggregateConsultancyReviewUseCase(BaseUseCase):
    def __init__(self,consultancy):
        self._consultancy = consultancy

    def execute(self):
        self._factory()
        return self.review

    def _factory(self):
        # pass
        self.review = list(ConsultancyReview.objects.filter(consultancy=self._consultancy).values("rating").\
            annotate(rating_count=Count("rating")))

class CreateConsultancyReviewUseCase(BaseUseCase):
    def __init__(self,student,serializer):
        self._serializer = serializer
        self._data = self._serializer.validated_data
        self._student =student

    def execute(self):
        self._factory()

    def _factory(self):
        try:
            ConsultancyReview.objects.create(
                student=self._student,
                **self._data
            )
        except Exception as e:
            raise ReviewAlreadyExist

class ListConsultancyReviewUseCase(BaseUseCase):
    def __init__(self,consultancy):
        self._consultancy = consultancy

    def execute(self):

        self._factory()
        return self._review

    def _factory(self):
        self._review = ConsultancyReview.objects.filter(consultancy=self._consultancy)



class UpdateConsultancyReviewUseCase(BaseUseCase):
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