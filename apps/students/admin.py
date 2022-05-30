from django.contrib import admin

# Register your models here.
from apps.students import models
from apps.core.admin import BaseModelAdmin


@admin.register(models.StudentModel)
class StudentAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'fullname',
    )

@admin.register(models.StudentAddress)
class StudentAddressAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'student',
    )

@admin.register(models.FavouriteInstitute)
class StudentFavouriteInstitute(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'student',
    )


@admin.register(models.InstituteViewers)
class StudentHistryAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'student',
        'institute',
    )
