from django.contrib import admin

from apps.core.admin import BaseModelAdmin
from apps.portal import models


@admin.register(models.PortalStaff)
class PortalStaffAdmin(BaseModelAdmin):
    pass
