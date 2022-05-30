from django.contrib import admin
from apps.core.admin import BaseModelAdmin
from apps.studentIdentity.models import Citizenship, Passport
# Register your models here.
@admin.register(Citizenship)
class InstituteCourseAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'student',
    )

@admin.register(Passport)
class InstituteCourseAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'student',
    )