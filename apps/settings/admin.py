from django.contrib import admin

from apps.core.admin import BaseModelAdmin
from apps.settings import models


# Register your models here.
@admin.register(models.Settings)
class PortalAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'color',
        'user',
    )
