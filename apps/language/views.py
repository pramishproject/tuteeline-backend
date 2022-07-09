from apps.language.mixins import LanguageMixins
from apps.language import usecases
from apps.students.mixins import StudentMixin
from apps.language.serializers import CreateLanguageSerializer, ListLanguageSerializer
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.core import generics
# Create your views here.
from apps.user.permissions import IsStudentUser


class CreateLanguageView(generics.CreateWithMessageAPIView,StudentMixin):

    serializer_class = CreateLanguageSerializer
    message = _('Create language successfully')
    permission_classes = (IsAuthenticated, IsStudentUser)

    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()

    def perform_create(self, serializer):
        return usecases.CreateLanguageUseCase(
            student= self.get_object(),
            serializer = serializer
        ).execute()


class GetLanguageView(generics.ListAPIView,StudentMixin):
    serializer_class = ListLanguageSerializer

    permission_classes = (IsAuthenticated, IsStudentUser)

    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()

    def get_queryset(self):
        return usecases.GetStudentLanguageUsecase(
            student=self.get_object()
        ).execute()

class UpdateLanguageView(generics.UpdateWithMessageAPIView,LanguageMixins):
    serializer_class = CreateLanguageSerializer
    message = _('upadete language successfully')
    permission_classes = (IsAuthenticated, IsStudentUser)

    def get_object(self):
        self.check_object_permissions(self.request, self.get_language().user)
        return self.get_language()

    def perform_update(self, serializer):
        return usecases.UpdateStudentLanguageUseCase(
            language=self.get_object(),
            serializer = serializer
        ).execute()


class DeleteLanguageView(generics.DestroyAPIView,LanguageMixins):
    message = _("delete successfully")
    permission_classes = (IsAuthenticated, IsStudentUser)

    def get_object(self):
        self.check_object_permissions(self.request, self.get_language().user)
        return self.get_language()

    def perform_destroy(self, instance):
        return usecases.DeleteLanguageUseCase(
            language=self.get_object()
        ).execute()