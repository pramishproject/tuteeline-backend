from django.contrib import admin

from apps.core.admin import BaseModelAdmin
from apps.institute_course.models import  Faculty, InstituteApply
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
        'institute',
    )
# @admin.register(AccessOfAcademicDocument)
# class AccessOfAcademicDocumentAdmin(BaseModelAdmin):
#     list_display = BaseModelAdmin.list_display + (
#         "course",
#         "academic",
#     )
# @admin.register(AccessStudentIdentity)
# class AccessStudentIdentityAdmin(BaseModelAdmin):
#     list_display = BaseModelAdmin.list_display + (
#         'course',
#         'citizenship',
#         'passport',
#     )
# @admin.register(AccessStudentLor)
# class AccessStudentLorAdmin(BaseModelAdmin):
#     list_display = BaseModelAdmin.list_display + (
#         'course',
#         'lor',
#     )
# @admin.register(AccessStudentEssay)
# class AccessStudentEssayAdmin(BaseModelAdmin):
#     list_display = BaseModelAdmin.list_display + (
#         'course',
#         'essay',
#     )
# @admin.register(AccessStudentSop)
# class AccessStudentSopAdmin(BaseModelAdmin):
#     list_display = BaseModelAdmin.list_display + (
#         'course',
#         'sop',
#     )

