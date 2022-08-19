from django.contrib import admin

from apps.core.admin import BaseModelAdmin
from apps.institute_course.models import Faculty, \
    InstituteApply, CheckStudentIdentity, \
    CheckedAcademicDocument, CheckedStudentEssay, CheckedStudentLor, CheckedStudentSop \
    , CommentApplicationInstitute, ApplyAction, ActionApplyByConsultancy, VoucherFile

from apps.institute_course.models import Course
from apps.institute_course.models import InstituteCourse

@admin.register(InstituteCourse)
class InstituteCourseAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'institute',
    )

@admin.register(Faculty)
class FacultyAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'name',
    )

@admin.register(Course)
class CourseAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'name',
    )

@admin.register(InstituteApply)
class InstituteApplyAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display  + (
        'institute','student'
    )

@admin.register(CheckedAcademicDocument)
class CheckedAcademicDocumentAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        "application",
        "academic",
    )


@admin.register(CheckStudentIdentity)
class CheckStudentIdentityAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'application',
        'citizenship',
        'passport',
    )
@admin.register(CheckedStudentLor)
class CheckedStudentLorAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'application',
        'lor',
    )

@admin.register(CheckedStudentEssay)
class CheckedStudentEssayAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'application',
        'essay',
    )
@admin.register(CheckedStudentSop)
class CheckedStudentEssayAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'application',
        'sop',
    )

@admin.register(CommentApplicationInstitute)
class ApplicationCommentsAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'application',
    )

@admin.register(ApplyAction)
class ApplyActionAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'apply',
    )

@admin.register(ActionApplyByConsultancy)
class ActionApplyByConsultancyAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'apply',
    )

@admin.register(VoucherFile)
class VoucherFileAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'apply',
    )