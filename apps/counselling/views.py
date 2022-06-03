from apps.core import generics
from apps.counselling import serializers, usecases
# Create your views here.
from apps.counselling.mixins import InstituteCounsellingMixin
from apps.institute.mixins import InstituteMixins
from apps.students.mixins import StudentMixin


class CreateInstituteCounselling(generics.CreateWithMessageAPIView,StudentMixin):
    """
    this endpoint is use to create institute counciling view 2022-05-31T19:16:51+0000
    """
    serializer_class = serializers.CreateInstituteCounsellingSerializer
    message = 'Created Counselling successfully'
    def get_object(self):
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

    def get_object(self):
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
        return usecases.AssignCounselorUseCase(
            counselling=self.get_object(),
            serializer=serializer
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
