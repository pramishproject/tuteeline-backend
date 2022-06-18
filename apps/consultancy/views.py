from django.utils.translation import gettext_lazy as _
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.permissions import AllowAny

from apps.consultancy import serializers, usecases, filtersets
from apps.consultancy.mixins import ConsultancyMixin, ConsultancyStaffMixin
from apps.consultancy.serializers import ConsultancyDetailSerializer
from apps.core import generics
from apps.user.mixins import ConsultancyUserMixin
from rest_framework import filters

class RegisterConsultancyView(generics.CreateWithMessageAPIView):
    """
    Use this end-point to register consultancy
    """
    parser_classes = (MultiPartParser, FileUploadParser,)
    message = _('Registered successfully')
    permission_classes = (AllowAny,)
    serializer_class = serializers.RegisterConsultancySerializer

    def perform_create(self, serializer):
        return usecases.RegisterConsultancyUseCase(
            serializer=serializer
        ).execute()


class CreateConsultancyStaffView(generics.CreateWithMessageAPIView, ConsultancyMixin):
    """
    Use this end-point to create  consultancy user
    """
    message = 'Consultancy staff created successfully'
    serializer_class = serializers.CreateConsultancyStaffSerializer
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, FileUploadParser,)

    def get_object(self):
        return self.get_consultancy()

    def perform_create(self, serializer):
        return usecases.CreateConsultancyStaffUseCase(
            serializer=serializer,
            consultancy=self.get_object()
        ).execute()


class ListConsultancyStaffView(generics.ListAPIView, ConsultancyMixin):
    """
    Use this endpoint to list all staff of particular consultancy
    """
    serializer_class = serializers.ListConsultancyStaffSerializer
    filterset_class = filtersets.ConsultancyStaffSearchFilter

    def get_object(self):
        return self.get_consultancy()

    def get_queryset(self):
        return usecases.ListConsultancyStaffUseCase(consultancy=self.get_object()).execute()

    no_content_error_message = _("No Consultancy staff at the moment.")

class ConsultancyDetail(generics.RetrieveAPIView,ConsultancyMixin):
    """"""

    serializer_class = ConsultancyDetailSerializer
    def get_object(self):
        return self.get_consultancy()

    def get_queryset(self):
        return usecases.GetConsultancyUseCase(
            consultancy_id=self.get_object()
        ).execute()

class ListConsultancyView(generics.ListAPIView):
    serializer_class = serializers.ListConsultancySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    def get_queryset(self):
        return usecases.ListConsultancyUseCase().execute()


class UpdateConsultancyStaffView(generics.UpdateWithMessageAPIView, ConsultancyStaffMixin):
    """
    Use this end point to update consultancy staff details
    """

    serializer_class = serializers.UpdateConsultancyStaffDetail
    message = _("Updated successfully")
    parser_classes = (MultiPartParser, FileUploadParser,)

    def get_object(self):
        return self.get_consultancy_staff()

    def perform_update(self, serializer):
        """
        CreateConsultancyStaffUseCaseUpdate is use for celery model
        """
        return usecases.CreateConsultancyStaffUseCase(
            serializer=serializer,
            consultancy_staff=self.get_object()
        ).execute()


class UpdateConsultancyStaffPhotoView(generics.UpdateWithMessageAPIView, ConsultancyStaffMixin):
    """
    Use this end point to update consultancy staff photo
    """

    serializer_class = serializers.UpdateConsultancyStaffProfilePhotoDetail
    message = _("Updated successfully")
    # permission_classes = (MultiPartParser,FileUploadParser,)
    parser_classes = (MultiPartParser, FileUploadParser,)

    def get_object(self):
        return self.get_consultancy_staff()

    def perform_update(self, serializer):
        return usecases.UpdateConsultancyStaffPhotoUseCase(
            serializer=serializer,
            consultancy_staff=self.get_object()
        ).execute()


class DeactivateConsultancyUserView(generics.CreateWithMessageAPIView, ConsultancyUserMixin):
    """
    Use this end point to deactivate  consultancy user
    """
    permission_classes = (AllowAny,)  # -> to be change
    message = _("User  deactivated successfully")
    serializer_class = serializers.DeactivateConsultancyUserSeralizer

    def get_object(self):
        return self.get_consultancy_user()

    def perform_create(self, serializer):
        return usecases.DeactivateConsultancyUserUseCase(
            serializer=serializer,
            consultancy_user=self.get_object()
        ).execute()


class ActivateConsultancyUserView(generics.CreateWithMessageAPIView, ConsultancyUserMixin):
    """
    Use this end point to activate  consultancy user
    """
    permission_classes = (AllowAny,)  # -> to be change
    message = _("User  activated successfully")
    serializer_class = serializers.ActivateConsultancyUserSeralizer

    def get_object(self):
        return self.get_consultancy_user()

    def perform_create(self, serializer):
        return usecases.ActivateConsultancyUserUseCase(
            serializer=serializer,
            consultancy_user=self.get_object()
        ).execute()
