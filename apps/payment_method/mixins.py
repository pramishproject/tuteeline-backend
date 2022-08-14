from apps.institute_course import usecases

class CourseMixin:
    def get_provider(self):
        return usecases.GetCourseUseCase(
            institute_course_id = self.kwargs.get('institute_course_id')
        ).execute()