from django.contrib import admin

# Register your models here.

from apps.core.admin import BaseModelAdmin
from apps.payment_method.models import Provider,VoucherPayment,ProviderName,Transaction

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

@admin.register(ProviderName)
class RelationAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display+(
        'name',
    )

@admin.register(Transaction)
class TransactionAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'student',
        'institute',
        'payment_method',
        'payment_type',
        'amount',
    )