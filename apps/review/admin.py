from django.contrib import admin

from apps.review import models
from apps.core.admin import BaseModelAdmin


@admin.register(models.InstituteReview)
class StudentAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'student',
        'institute',
        'review', 
        'rating',
    )