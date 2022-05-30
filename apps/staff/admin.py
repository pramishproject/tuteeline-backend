from django.contrib import admin

# Register your models here.
from apps.core.admin import BaseModelAdmin
from apps.staff import models


@admin.register(models.StaffPosition)
class StaffPositionAdmin(BaseModelAdmin):
    pass
