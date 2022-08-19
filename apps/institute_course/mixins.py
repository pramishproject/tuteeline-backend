from apps.institute_course import usecases

class CourseMixin:
    def get_institutecourse(self):
        return usecases.GetCourseUseCase(
            institute_course_id = self.kwargs.get('institute_course_id')
        ).execute()

class FacultyMixin:
    def get_faculty(self):
        return usecases.GetFacultyUseCase(
            faculty_id = self.kwargs.get('faculty_id')
        ).execute()

class ApplyMixin:
    def get_apply(self):
        return usecases.GetApplyInstitute(
            apply_id=self.kwargs.get("apply_id")
        ).execute()

class VoucherFileMixin:
    def get_voucher(self):
        return usecases.GetVoucherFileUseCase(
            voucher_id=self.kwargs.get('voucher_id')
        ).execute()