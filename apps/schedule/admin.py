from django.contrib import admin

# Register your models here.
from apps.core.admin import BaseModelAdmin
from apps.schedule import models


@admin.register(models.CounsellingSchedule)
class ConsultancyAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'title',
        # 'counselor',
        'status'
    )
    list_filter = (
        'status',

    )

@admin.register(models.Booking)
class ConsultancyAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'note',
        'schedule',
        'is_booked'
    )
    list_filter = (
        'note',

    )
