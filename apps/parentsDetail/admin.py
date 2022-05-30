from django.contrib import admin

from apps.core.admin import BaseModelAdmin
from apps.parentsDetail import models

@admin.register(models.StudentParents)
class StudentParentsAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display+(
        'student',
    )
