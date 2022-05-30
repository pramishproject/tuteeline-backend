from django.contrib import admin

from apps.institute import models
from apps.core.admin import BaseModelAdmin


# Register your models here.
@admin.register(models.Institute)
class InstituteAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'name',
    )


@admin.register(models.InstituteStaff)
class InstituteStaffAdmin(BaseModelAdmin):
    list_filter = BaseModelAdmin.list_filter+(
        'institute',
    )   

@admin.register(models.InstituteScholorship)
class ScholorshipAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'topic',
    )

@admin.register(models.SocialMediaLink)
class SocialMediaAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display+(
        'name',
    )

@admin.register(models.AddInstituteFacility)
class InstituteFacility(BaseModelAdmin):
    list_filter = BaseModelAdmin.list_filter+(
        'institute',
    )


@admin.register(models.Facility)
class Facility(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + (
        'name',
    )