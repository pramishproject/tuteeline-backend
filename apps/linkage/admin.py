from django.contrib import admin
from apps.linkage.models import Linkage
from apps.core.admin import BaseModelAdmin
# Register your models here.
@admin.register(Linkage)
class LinkageAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'institute','consultancy'
    )