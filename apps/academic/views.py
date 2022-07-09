from apps.academic.mixins import AcademicMixins, GetSopMixin, GetEssayMixins, LorMixins
from rest_framework.serializers import Serializer
from apps.academic.serializers import (CreateAcademicSerializer, CreateLorSerializer, CreateSopSerializer,
CreateEssaySerializer, GetAcademicListSerializer, GetLorSerializer, GetPersonalEssay, GetSopSerializer, UpdateCertificateSerializer, UpdateMarksheetSerializer, UpdateSopSerializer,
UpdateAcademicSerializer,UpdateEssaySerializer)
from django.utils.translation import gettext_lazy as _
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.core import generics
from apps.students.mixins import StudentMixin
from apps.students import mixins
from apps.academic import usecases
# Create your views here.
from apps.user.permissions import IsStudentUser


class CreateAcademicView(generics.CreateWithMessageAPIView,StudentMixin):
    """
    use this endpoint to add academic detail
    """
    parser_classes = (MultiPartParser, FileUploadParser,)
    serializer_class = CreateAcademicSerializer
    message = _("Academic Detail added successfully")
    permission_classes = (IsAuthenticated, IsStudentUser)

    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()

    def perform_create(self, serializer):
        return usecases.CreateStudentAcademicUseCase(
            student=self.get_object(),
            serializer=serializer
        ).execute()


class GetAcademicListView(generics.ListAPIView,StudentMixin):
    """
    this endpoint is use to get academic list
    """
    serializer_class = GetAcademicListSerializer
    no_content_error_message = _('no academic detail at that moment')
    permission_classes = (IsAuthenticated, IsStudentUser)

    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()

    def get_queryset(self):
        return usecases.GetAcademicListUseCase(
            student=self.get_object()
        ).execute()


class UpdateAcademicView(generics.UpdateWithMessageAPIView,AcademicMixins):
    """
    This endpoint is use to find academic list of student
    """
    serializer_class = UpdateAcademicSerializer
    parser_classes = (MultiPartParser , FileUploadParser, )
    message = _("academic detail update successfully")

    permission_classes = (IsAuthenticated, IsStudentUser)

    def get_object(self):
        self.check_object_permissions(self.request, self.get_academic().student.user)
        return self.get_academic()

    def perform_update(self, serializer):
        return usecases.UpdateAcademicUseCase(
            academic=self.get_object(),
            serializer=serializer
        ).execute()

class UpdateMarksheetView(generics.UpdateWithMessageAPIView,AcademicMixins):
    """
    This endpoint is use to update marksheet file
    """
    serializer_class = UpdateMarksheetSerializer
    parser_classes = (MultiPartParser , FileUploadParser, )
    message = _("marksheet update successfully")

    permission_classes = (IsAuthenticated, IsStudentUser)

    def get_object(self):
        self.check_object_permissions(self.request, self.get_academic().student.user)
        return self.get_academic()

    def perform_update(self, serializer):
        return usecases.UpdateAcademicUseCase(
            academic=self.get_object(),
            serializer=serializer
        ).execute()

class UpdateCertificateView(generics.UpdateWithMessageAPIView,AcademicMixins):
    """
    This endpoint is use to update certificate
    """
    serializer_class = UpdateCertificateSerializer
    parser_classes = (MultiPartParser , FileUploadParser, )
    message = _("marksheet update successfully")

    permission_classes = (IsAuthenticated, IsStudentUser)

    def get_object(self):
        self.check_object_permissions(self.request, self.get_academic().student.user)
        return self.get_academic()

    def perform_update(self, serializer):
        return usecases.UpdateAcademicUseCase(
            academic=self.get_object(),
            serializer=serializer
        ).execute()

        
class CreateSopView(generics.CreateWithMessageAPIView,StudentMixin):
    """
    use this endpoint to add sop one student can add one sop
    """
    permission_classes = (AllowAny ,)
    parser_classes = (MultiPartParser , FileUploadParser, )
    serializer_class = CreateSopSerializer
    message = _("SOP Add successfully")
    permission_classes = (IsAuthenticated, IsStudentUser)

    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()

    def perform_create(self, serializer):
        return usecases.CreateStudentSopUseCase(
            student = self.get_object(),
            serializer =serializer
        ).execute()


class CreateLorView(generics.CreateWithMessageAPIView,StudentMixin):
    """
    use this endpoint to add lor ons student can add more then one lor
    """
    parser_classes = (MultiPartParser , FileUploadParser, )
    serializer_class = CreateLorSerializer
    message = _("Lor Add successfully")

    permission_classes = (IsAuthenticated, IsStudentUser)

    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()

    def perform_create(self, serializer):
        return usecases.CreateStudentLorUseCase(
            student = self.get_object(),
            serializer =serializer
        ).execute()

class DeleteLorView(generics.DestroyWithMessageAPIView,LorMixins):
    permission_classes = (IsAuthenticated, IsStudentUser)

    def get_object(self):
        self.check_object_permissions(self.request, self.get_lor().student.user)
        return self.get_lor()
    def perform_destroy(self, instance):
        return usecases.DeleteLorUseCase(
            lor=self.get_lor()
        ).execute()

class UpdateLorView(generics.UpdateWithMessageAPIView,LorMixins): #todo
    pass

class CreatePersonalEssayView(generics.CreateWithMessageAPIView,StudentMixin):
    """
    use this endpoint to add student personal essay one student can add one essay
    """
    parser_classes = (MultiPartParser , FileUploadParser, )
    serializer_class = CreateEssaySerializer
    message = _("personal essay Add successfully ")
    permission_classes = (IsAuthenticated, IsStudentUser)

    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()

    def perform_create(self, serializer):
        return usecases.CreateStudentEssayUseCase(
            student = self.get_object(),
            serializer =serializer
        ).execute()

class GetSopView(generics.ListAPIView,StudentMixin):
    """
    This endpoint is use to get sop
    """
    parser_classes = (MultiPartParser , FileUploadParser, )
    serializer_class = GetSopSerializer
    no_content_error_message = _('no academic detail at that moment')
    permission_classes = (IsAuthenticated, IsStudentUser)

    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()

    def get_queryset(self):
        return usecases.GetStudentSopUseCase(
            student=self.get_object()
        ).execute()


class GetLorListView(generics.ListAPIView,StudentMixin):
    """
    This endpoint is use to get sudent lor
    """
    parser_classes = (MultiPartParser , FileUploadParser, )
    serializer_class = GetLorSerializer
    no_content_error_message = _('no academic detail at that moment')
    permission_classes = (IsAuthenticated, IsStudentUser)

    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()

    def get_queryset(self):
        return usecases.GetLorListUseCase(
            student=self.get_object()
        ).execute()

class GetEssayView(generics.ListAPIView,StudentMixin):
    """
    This endpoint is use to get student personal essay
    """
    serializer_class = GetPersonalEssay
    permission_classes = (IsAuthenticated, IsStudentUser)

    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()

    def get_queryset(self):
        return usecases.GetPersonalEssayUseCase(
            student=self.get_object()
        ).execute()

class UpdateSopView(generics.UpdateWithMessageAPIView,GetSopMixin):
    """
    This endpoint is use to find academic list of student
    """
    serializer_class = UpdateSopSerializer
    parser_classes = (MultiPartParser , FileUploadParser, )
    message = _("sop detail update successfully")
    permission_classes = (IsAuthenticated, IsStudentUser)

    def get_object(self):
        self.check_object_permissions(self.request, self.get_sop().student.user)
        return self.get_sop()

    def perform_update(self, serializer):
        return usecases.UpdateSopUseCase(
            serializer=serializer,
            id=self.get_object(),
            
        ).execute()


class DeleteSopView(generics.DestroyAPIView,GetSopMixin):
    message = _("delete successfully")
    permission_classes = (IsAuthenticated, IsStudentUser)

    def get_object(self):
        self.check_object_permissions(self.request, self.get_sop().student.user)
        return self.get_sop()

    def perform_destroy(self, instance):
        return usecases.DeleteSopUseCase(
            sop=self.get_object()
        ).execute()

class UpdateEssayView(generics.UpdateWithMessageAPIView,GetEssayMixins):
    serializer_class = UpdateEssaySerializer
    parser_classes = (MultiPartParser , FileUploadParser, )
    message = _("update essay successfully")
    permission_classes = (IsAuthenticated, IsStudentUser)

    def get_object(self):
        self.check_object_permissions(self.request, self.get_essay().student.user)
        return self.get_essay()

    def perform_update(self, serializer):
        return usecases.UpdateEssayUseCase(
            serializer=serializer,
            essay=self.get_object(),
        ).execute()


class DeleteEssayView(generics.DestroyAPIView,GetEssayMixins):
    message = _("delete successfully")
    permission_classes = (IsAuthenticated, IsStudentUser)

    def get_object(self):
        self.check_object_permissions(self.request, self.get_essay().student.user)
        return self.get_essay()

    def perform_destroy(self, instance):
        return usecases.DeleteEssayUseCase(
            essay=self.get_object()
        ).execute()


class DeleteAcademicView(generics.DestroyAPIView,AcademicMixins):
    """
    This endpoint is use to find academic list of student
    """
    message = _("delete successfully")
    permission_classes = (IsAuthenticated, IsStudentUser)

    def get_object(self):
        self.check_object_permissions(self.request, self.get_academic().student.user)
        return self.get_academic()

    def perform_update(self, instance):
        return usecases.DeleteAcademicUseCase(
            academic=self.get_object(),
        ).execute()