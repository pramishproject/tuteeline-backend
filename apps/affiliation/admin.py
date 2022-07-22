from django.contrib import admin
from apps.affiliation import models
from apps.core.admin import BaseModelAdmin
# Register your models here.
@admin.register(models.Affiliation)
class AffiliationAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'institute',
        'university',
    )