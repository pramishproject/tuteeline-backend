from django.contrib import admin
from apps.consultancy_course import models
from apps.core.admin import  BaseModelAdmin
@admin.register(models.ConsultancyCourse)
class ConsultancyCourseAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'course',
    )
