from django.db.models.deletion import CASCADE
from apps.students.models import StudentModel
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from apps.core import fields
from apps.core.models import BaseModel
from apps.core.validators import validate_image

class Language(BaseModel):
    student = models.ForeignKey(
        StudentModel,
        on_delete=CASCADE
    )
    name = models.CharField(max_length=100)
    first_language = models.BooleanField(default=False)
    speak = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    write = models.BooleanField(default=False)
    spoken_at_home= models.BooleanField(default=False)

    class Meta:
        unique_together= ('student','name')


