from apps.consultancy.mixins import ConsultancyMixin
from apps.core import generics
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import AllowAny
from apps.institute.mixins import InstituteMixins
from apps.review.mixins import InstituteReviewMixins, ConsultancyReviewMixins
from apps.review.serializers import CreateInstituteReviewSerializer, ListInstituteReviewSerializer, \
    UpdateInstituteReviewSerializer, InstituteAggregateReviewSerializer, CreateConsultancyReviewSerializer, \
    ListConsultancyReviewSerializer, UpdateConsultancyReviewSerializer
from apps.review.usecases import GetConsultancyReviewByIdUseCase
from apps.students.mixins import StudentMixin
from apps.review import usecases
# Create your views here.

class CreateInstituteReviewView(generics.CreateWithMessageAPIView,StudentMixin):

    serializer_class = CreateInstituteReviewSerializer
    message = _('Create review successfully')
    permission_classes = (AllowAny,)

    def get_object(self):
        return self.get_student()

    def perform_create(self, serializer):
        return usecases.CreateInstituteReviewUseCase(
            student= self.get_object(),
            serializer = serializer
        ).execute()

class UpdateInstituteReviewView(generics.UpdateWithMessageAPIView,InstituteReviewMixins):
    serializer_class = UpdateInstituteReviewSerializer
    message = _('Update review Successfully')
    permission_classes = (AllowAny,)
    def get_object(self):
        return self.get_Institute_review()

    def perform_update(self, serializer):
        return usecases.UpdateInstituteReviewUseCase(
            review=self.get_object(),
            serializer = serializer
        ).execute()

class ListInstituteReviewView(generics.ListAPIView,InstituteMixins):
    serializer_class = ListInstituteReviewSerializer
    def get_object(self):
        return self.get_institute()

    def get_queryset(self):
        return usecases.ListInstituteReviewUseCase(
            institute=self.get_object()
        ).execute()

    def get_serializer_context(self):
        context = super(ListInstituteReviewView, self).get_serializer_context()
        context.update({"request": self.request})
        return context

class GetInstituteAggregateReviewView(generics.ListAPIView,InstituteMixins):
    serializer_class = InstituteAggregateReviewSerializer
    def get_object(self):
        return self.get_institute()

    def get_queryset(self):
        return usecases.GetAggregateInstituteReviewUseCase(institute=self.get_object()).execute()



# --------------------------------consultancy review ------------

class CreateConsultancyReviewView(generics.CreateAPIView,StudentMixin):
    serializer_class = CreateConsultancyReviewSerializer

    def get_object(self):
        return self.get_student()

    def perform_create(self, serializer):
        return usecases.CreateConsultancyReviewUseCase(
            student=self.get_object(),
            serializer =serializer
        ).execute()

class ListConsultancyReview(generics.ListAPIView,ConsultancyMixin):
    serializer_class = ListConsultancyReviewSerializer

    def get_object(self):
        return self.get_consultancy()

    def get_queryset(self):
        return usecases.ListConsultancyReviewUseCase(
            consultancy=self.get_object(),
        ).execute()

    def get_serializer_context(self):
        context = super(ListConsultancyReview, self).get_serializer_context()
        context.update({"request": self.request})
        return context

class UpdateConsultancyReview(generics.UpdateAPIView,ConsultancyReviewMixins):

    serializer_class = UpdateConsultancyReviewSerializer

    def get_object(self):
        return self.get_consultancy_review()

    def perform_update(self, serializer):
        return usecases.UpdateConsultancyReviewUseCase(
            review=self.get_object(),
            serializer = serializer
        ).execute()