from django.contrib import admin

from apps.consultancy import models
from apps.core.admin import BaseModelAdmin


@admin.register(models.Consultancy)
class ConsultancyAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'name',
    )


@admin.register(models.ConsultancyStaff)
class ConsultancyStaffAdmin(BaseModelAdmin):
    list_filter = BaseModelAdmin.list_filter+(
        'consultancy',
    )


