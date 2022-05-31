from apps.core import generics
from apps.counselling import serializers, usecases
# Create your views here.
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

