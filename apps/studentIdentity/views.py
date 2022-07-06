from rest_framework.permissions import IsAuthenticated

from apps.studentIdentity.mixins import CitizenshipMixins, PassportMixins
from rest_framework import serializers
from apps.students.mixins import StudentMixin
from apps.studentIdentity.serializers import (GetCitizenshipSerializer, 
GetPassportSerializer, StudentCitizenshipSerializer, StudentPassportSerializer, 
UpdateCitizenshipBackSerializer, UpdateCitizenshipCharacterSerialzer,UpdateCitizenshipFrontSerializer,
StudentPassportUpdateSerializer,
PasswordImageUpdateSerializer)
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from apps.studentIdentity import usecases
from apps.core import generics

# Create your views here.
from apps.user.permissions import IsStudentUser


class AddCitizenshipView(generics.CreateWithMessageAPIView , StudentMixin):
    serializer_class = StudentCitizenshipSerializer
    message = _("add citizenship successfully")
    permission_classes = (IsAuthenticated, IsStudentUser)
    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()


    def perform_create(self, serializer):
        return usecases.AddCitizenshipUseCase(
            serializer = serializer,
            student_id = self.get_object()
        ).execute()

class AddPassportView(generics.CreateWithMessageAPIView,StudentMixin):
    """
    Add passport endpoint
    """
    serializer_class = StudentPassportSerializer
    message = _("add passport successfully")
    permission_classes = (IsAuthenticated, IsStudentUser)
    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()

    def perform_create(self, serializer):
        return usecases.AddPassportUseCase(
            student_id=self.get_object(),
            serializer=serializer
        ).execute()
        

class GetCitizenshipView(generics.RetrieveAPIView,CitizenshipMixins):
    """
    this endpoint is use to find student citizenship
    """
    serializer_class =GetCitizenshipSerializer
    permission_classes = (IsAuthenticated, IsStudentUser)
    def get_object(self):
        self.check_object_permissions(self.request, self.get_citizenship().student.user)
        return self.get_citizenship()

    def get_queryset(self):
        return usecases.GetStudentCitizenshipUseCase(
            citizenship=self.get_object()
        ).execute()

class GetPassportView(generics.RetrieveAPIView,PassportMixins):
    """
    this endpoint is use to find student citizenship
    """
    serializer_class = GetPassportSerializer
    permission_classes = (IsAuthenticated, IsStudentUser)
    def get_object(self):
        self.check_object_permissions(self.request, self.get_passport().student.user)
        return self.get_passport()

    def get_queryset(self):
        return usecases.GetStudentPassportUseCase(
            passport=self.get_object()
        ).execute()


class UpdateCitizenshipFrontPageView(generics.UpdateWithMessageAPIView,CitizenshipMixins):
    """
    this endpoint is use to update frontpage
    """
    serializer_class = UpdateCitizenshipFrontSerializer
    permission_classes = (IsAuthenticated, IsStudentUser)
    def get_object(self):
        self.check_object_permissions(self.request, self.get_citizenship().student.user)
        return self.get_citizenship()

    def perform_update(self, serializer):
        return usecases.UpdateCitizenshipUseCase(
            serializer=serializer,
            citizenship=self.get_object()
        ).execute()


class UpdateCitizenshipBackPageView(generics.UpdateWithMessageAPIView,CitizenshipMixins):
    """
    this endpoint is use to update frontpage
    """
    serializer_class = UpdateCitizenshipBackSerializer
    permission_classes = (IsAuthenticated, IsStudentUser)
    def get_object(self):
        self.check_object_permissions(self.request, self.get_citizenship().student.user)
        return self.get_citizenship()

    def perform_update(self, serializer):
        return usecases.UpdateCitizenshipUseCase(
            serializer=serializer,
            citizenship=self.get_object()
        ).execute()

class UpdateCitizenshipView(generics.UpdateWithMessageAPIView,CitizenshipMixins):
    """
    update citizenship
    """
    serializer_class = UpdateCitizenshipCharacterSerialzer
    permission_classes = (IsAuthenticated, IsStudentUser)
    def get_object(self):
        self.check_object_permissions(self.request, self.get_citizenship().student.user)
        return self.get_citizenship()

    def perform_update(self, serializer):
        return usecases.UpdateCitizenshipUseCase(
            serializer=serializer,
            citizenship=self.get_object()
        ).execute()


class UpdatePassportImageView(generics.UpdateWithMessageAPIView,PassportMixins):
    """
    update passport image
    """
    serializer_class = PasswordImageUpdateSerializer
    permission_classes = (IsAuthenticated, IsStudentUser)
    def get_object(self):
        self.check_object_permissions(self.request, self.get_passport().student.user)
        return self.get_passport()

    def perform_update(self, serializer):
        return usecases.UpdatePassportUseCase(
            serializer=serializer,
            passport=self.get_object()
        ).execute()

class UpdatePassportView(generics.UpdateWithMessageAPIView,PassportMixins):
    """
    update passport
    """
    serializer_class = StudentPassportUpdateSerializer
    permission_classes = (IsAuthenticated, IsStudentUser)
    def get_object(self):
        self.check_object_permissions(self.request, self.get_passport().student.user)
        return self.get_passport()

    def perform_update(self, serializer):
        return usecases.UpdatePassportUseCase(
            serializer=serializer,
            passport=self.get_object()
        ).execute()