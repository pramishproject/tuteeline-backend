from apps.consultancy_course.usecases import GetConsultancyCourse

class ConsultancyCourseMixin:
    def get_consultancy_course(self):
        return GetConsultancyCourse(
            consultancy_course_id=self.kwargs.get('consultancy_course_id')
        ).execute()