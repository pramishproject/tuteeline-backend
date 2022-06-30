from apps.consultancy_course.exceptions import ConsultancyCourseNotFound
from apps.consultancy_course.models import ConsultancyCourse
from apps.core.usecases import BaseUseCase

class GetConsultancyCourse(BaseUseCase):
    def __init__(self,consultancy_course_id):
        self._course_id = consultancy_course_id

    def execute(self):
        self._factory()
        return self._course

    def _factory(self):
        try:
            self._course=ConsultancyCourse.objects.get(pk=self._course_id)
        except ConsultancyCourse.DoesNotExist:
            raise ConsultancyCourseNotFound
