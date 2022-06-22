from apps.parentsDetail.mixins import ParentsMixin
from apps.parentsDetail.serializers import GetParentsListSerializer, ParentsDetailSerializer, UpdateParentsDetailSerializer
from django.utils.translation import gettext_lazy as _
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.permissions import AllowAny

from apps.core import generics
from apps.students.mixins import StudentMixin
from apps.parentsDetail import usecases



# AddParentsUseCase
class AddParentsView(generics.CreateWithMessageAPIView,StudentMixin):
    """
    Add Parents endpoint
    """
    serializer_class = ParentsDetailSerializer
    message = _("add parents successfully")

    def get_object(self):
        return self.get_student()

    def perform_create(self, serializer):
        return usecases.AddParentsUseCase(
            serializer=serializer,
            student=self.get_object()
        ).execute()


class UpdateParentsView(generics.UpdateWithMessageAPIView,ParentsMixin):
    """
    update parents endpoint
    """
    serializer_class = UpdateParentsDetailSerializer
    message  = _("update parents successfully")

    def get_object(self):
        return self.get_parents()

    def perform_update(self, serializer):
        return usecases.UpdateParentsUseCase(
            serializer = serializer,
            parents = self.get_object()
        ).execute()

class DeleteParentsView(generics.DestroyWithMessageAPIView,ParentsMixin):
    """Delete parents api"""
    def get_object(self):
        return self.get_parents()

    def perform_destroy(self, instance):
        return usecases.DeleteParentsUseCase(
            parents=self.get_object(),
        ).execute()


class GetParentsView(generics.ListAPIView,StudentMixin):
    """
    use this endpont to list of parents
    """
    serializer_class = GetParentsListSerializer
    no_content_error_message = _('No parents at that moment')
    def get_object(self):
        return self.get_student()

    def get_queryset(self):
        return usecases.GetStudentParentsUseCase(
            student=self.get_object()
        ).execute()

