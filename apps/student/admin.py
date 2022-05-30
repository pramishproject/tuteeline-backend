from django.contrib import admin
from .models import Parents, AcademicInfo, StudentApply

admin.site.register((Parents, AcademicInfo, StudentApply))
