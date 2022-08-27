from django.contrib import admin

# Register your models here.

from apps.core.admin import BaseModelAdmin
from apps.payment_method.models import Provider,VoucherPayment

#
@admin.register(Provider)
class RelationAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display+(
        'provider_id',
    )

@admin.register(VoucherPayment)
class RelationAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display+(
        'bank_name',
    )