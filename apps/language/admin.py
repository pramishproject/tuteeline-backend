from django.contrib import admin

from apps.language import models
from apps.core.admin import BaseModelAdmin


@admin.register(models.Language)
class ConsultancyAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'name',
    )

