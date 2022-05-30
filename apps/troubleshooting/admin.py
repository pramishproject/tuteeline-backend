from django.contrib import admin

# Register your models here.
from apps.core.admin import BaseModelAdmin
from apps.troubleshooting import models


@admin.register(models.Troubleshoot)
class BillingTroubleShootAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display+(
        'status',
        'assigned_by',
        'assigned_to',
    )

    list_filter = (
        'status',
        'assigned_by',
        'assigned_to',
    )
#

@admin.register(models.BillingTroubleshoot)
class BillingTroubleShootAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'type',
        'category',
        'trouble_shot',
    )


