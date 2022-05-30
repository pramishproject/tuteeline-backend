from django.contrib import admin

from apps.core.admin import BaseModelAdmin
from apps.academic import models


@admin.register(models.Academic)
class AcademicAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'student',
    )

@admin.register(models.StudentLor)
class StudentLorAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'student',
    )

@admin.register(models.StudentSop)
class SopAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'student',
    )

@admin.register(models.PersonalEssay)
class PersonalEssayAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'student',
    )
