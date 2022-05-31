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

