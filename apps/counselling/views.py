from rest_framework.permissions import IsAuthenticated

from apps.consultancy.mixins import ConsultancyMixin, ConsultancyStaffMixin
from apps.core import generics
from apps.counselling import serializers, usecases
# Create your views here.
from apps.counselling.mixins import InstituteCounsellingMixin, ConsultancyCounsellingMixin
from apps.counselling.models import TestJson
from apps.institute.mixins import InstituteMixins, InstituteStaffMixins
from apps.students.mixins import StudentMixin
from apps.user.permissions import IsStudentUser


class CreateInstituteCounselling(generics.CreateAPIView,StudentMixin):
    """
    this endpoint is use to create institute counciling view 2022-05-31T19:16:51+0000
    """
    serializer_class = serializers.CreateInstituteCounsellingSerializer
    message = 'Created Counselling successfully'
    permission_classes = (IsAuthenticated, IsStudentUser)
    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()

    def perform_create(self, serializer):
        return usecases.CreateInstituteCounsellingUseCase(
            student=self.get_object(),
            serializer=serializer,
        ).execute()

class StudentCounsellingList(generics.ListAPIView,StudentMixin):
    """
    This end point is use to list student counciling view
    """
    serializer_class = serializers.ListStudentCounsellingSerializer
    permission_classes = (IsAuthenticated, IsStudentUser)
    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()

    def get_queryset(self):
        return usecases.ListStudentCounsellingUseCase(
            student=self.get_object()
        ).execute()

class StudentCounsellingListForInstitute(generics.ListAPIView,InstituteMixins):

    """
    This endpoint is use to list student counseling
    """
    serializer_class = serializers.ListInstituteCounsellingSerializer
    def get_object(self):
        return self.get_institute()

    def get_queryset(self):
        return usecases.ListStudentCounsellingForInstituteUseCase(
            institute=self.get_object()
        ).execute()


class AssignCounsellingStudent(generics.UpdateWithMessageAPIView,InstituteCounsellingMixin):
    """
    Assign student
    """
    serializer_class = serializers.AssignCounselorUserSerializer
    def get_object(self):
        return self.get_counselling()

    def get_queryset(self,serializer):
        return usecases.UpdateCounsellingUseCase(
            counselling=self.get_object(),
            serializer=serializer
        ).execute()

class InstituteCounsellingDetail(generics.RetrieveAPIView,InstituteCounsellingMixin):
    """
    institute counselling detail
    """
    serializer_class = serializers.InstituteCounsellingDetail
    def get_object(self):
        return self.get_counselling()

    def get_queryset(self):
        return usecases.GetInstituteCounsellingDetailUseCase(
            counselling=self.get_object()
        ).execute()

class AddNotesView(generics.UpdateWithMessageAPIView,InstituteCounsellingMixin):
    """
    update Notice
    """
    serializer_class = serializers.AddNotesSerializer
    def get_object(self):
        return self.get_counselling()

    def get_queryset(self,serializer):
        return usecases.AssignCounselorUseCase(
            counselling=self.get_object(),
            serializer=serializer
        ).execute()

class AssignCouncilingListView(generics.ListAPIView,InstituteStaffMixins): #todo this is use to list counciling for institute user
    serializer_class = serializers.ListInstituteStaffCounsellingSerializer

    def get_object(self):
        return self.get_institute_staff()

    def get_queryset(self):
        return usecases.ListCounselingInstituteStaffUseCase(
            staff=self.get_object()
        ).execute()

class ActionCounsellingView(generics.UpdateWithMessageAPIView,InstituteCounsellingMixin):
    serializer_class = serializers.ActionCounselling

    def get_object(self):
        return self.get_counselling()

    def perform_update(self, serializer):
        return  usecases.UpdateCounsellingUseCase(
            counselling=self.get_object(),
            serializer=serializer
        ).execute()
# consultancy counciling mixin---------------

class CreateConsultancyCounselling(generics.CreateAPIView,StudentMixin):
    """
    This endpoint is use to crate consultancy counselling 2022-05-31T19:16:51+0000
    """
    serializer_class = serializers.CreateConsultancyCounsellingSerializer
    permission_classes = (IsAuthenticated, IsStudentUser)

    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()

    def perform_create(self, serializer):
        return usecases.CreateConsultancyCounsellingUseCase(
            student=self.get_object(),
            serializer=serializer
        ).execute()

class ListConsultancyCounsellingForStudent(generics.ListAPIView,StudentMixin):
    """
    This api is use to list counseltancy counselling
    """
    serializer_class = serializers.ListStudentCounsellingOfConsultancySerializer
    permission_classes = (IsAuthenticated, IsStudentUser)

    def get_object(self):
        self.check_object_permissions(self.request, self.get_student().user)
        return self.get_student()

    def get_queryset(self):
        return usecases.ListConsultancyCounsellingForStudentUseCase(
            student=self.get_object()
        ).execute()

class AddConsultancyNotes(generics.UpdateWithMessageAPIView,ConsultancyCounsellingMixin): #todo
    serializer_class = serializers.UpdateConsultancyUser

    def get_object(self):
        return self.get_consultancy_staff()

    def perform_update(self, serializer):
        return usecases.UpdateCounsellingUseCase(
            counselling=self.get_object(),
            serializer=serializer
        ).execute()

class ListConsultancyCounselling(generics.ListAPIView,ConsultancyMixin): #todo
    pass

class ListAssignConsultancyStaffCounselling(generics.ListAPIView,ConsultancyStaffMixin): #todo
    pass


class TestJsonView(generics.CreateAPIView):
    serializer_class = serializers.TestJsonSerializer
    def perform_create(self, serializer):
        self._serializer = serializer.validated_data
        print("alldate",TestJson.objects.all())
        print("data***********",self._serializer)
        TestJson.objects.create(**self._serializer)
