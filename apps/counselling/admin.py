from django.contrib import admin

from apps.core.admin import BaseModelAdmin
from apps.counselling.models import InstituteCounselling,InterestedCourse,ConsultancyCounselling
# Register your models here.
@admin.register(InstituteCounselling)
class CouncellingAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'institute','student'
    )

@admin.register(InterestedCourse)
class InterestedCourseAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'counselling','course'
    )

@admin.register(ConsultancyCounselling)
class ConsultancyCounsellingAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'consultancy','student','which_time'
    )