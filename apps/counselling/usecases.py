from datetime import datetime

from apps.core.usecases import BaseUseCase
from apps.counselling.models import InstituteCounselling,InterestedCourse
from apps.utils.string_to_json import StringToJson
from apps.students.models import StudentModel
from apps.utils.uuid_validation import is_valid_uuid


class CreateInstituteCounsellingUseCase(BaseUseCase):
    def __init__(self,student:StudentModel,serializer):
        self._student = student
        self._data = serializer.validated_data

    def execute(self):

        self._factory()

    def _factory(self):
        counciling =InstituteCounselling.objects.create(
            student=self._student,
            **self._data
        )
        bulk_interested_course = []
        course_id_list = StringToJson(data=self._data.pop('interested_courses')).execute()
        for courseId  in course_id_list:
            if is_valid_uuid(courseId):
                bulk_interested_course.append({
                    "counselling":counciling,
                    "course":courseId
                })
        InterestedCourse.objects.bulk_create(bulk_interested_course)


class GetCounselling(BaseUseCase):
    def __init__(self,counselling_id):
        self._counselling_id = counselling_id

    def execute(self):
        self._factory()
        return self._counselling

    def _factory(self):
        self._counselling = InstituteCounselling.objects.get(pk=self._counselling_id)

class ListStudentCounsellingUseCase(BaseUseCase):
    def __init__(self,student:StudentModel):
        self._student = student

    def execute(self):
        self._factory()
        return self._counselling

    def _factory(self):
        self._counselling = InstituteCounselling.objects.filter(student=self._student).prefetch_related("institute")


class ListStudentCounsellingForInstituteUseCase(BaseUseCase):
    def __init__(self,institute):
        self._institute=institute

    def execute(self):
        self._factory()
        return self._counselling

    def _factory(self):
        self._counselling =InstituteCounselling.objects.filter(institute=self._institute).prefetch_related("student","assign_to")


class AssignCounselorUseCase(BaseUseCase):
    def __init__(self,counselling,serializer):
        self._counselling = counselling
        self._data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        for key in self._data.keys():
            setattr(self._counselling,key,self._data.get(key))

        self._counselling.updated_at = datetime.now()
        self._counselling.save()

