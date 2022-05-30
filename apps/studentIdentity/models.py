from django.db.models.deletion import CASCADE
# from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
import datetime
from rest_framework.exceptions import ValidationError

from apps.students.models import StudentModel
from apps.studentIdentity.utils import upload_student_identity_image_to
from apps.core import fields
from apps.core.models import BaseModel
from apps.core.validators import validate_image

# Create your models here.
class Citizenship(BaseModel):
    student = models.OneToOneField(StudentModel,on_delete=CASCADE)
    citizenship_number = models.CharField(max_length=200,blank=True)
    issue_date = models.DateField(blank=True)
    issue_from = models.CharField(max_length=200,blank=True)
    front_page = models.ImageField(
        upload_to = upload_student_identity_image_to,
        validators=[validate_image]
    )
    back_page = models.ImageField(
        upload_to = upload_student_identity_image_to,
        validators=[validate_image]
    )
    def save(self, *args ,**kwargs):
        if self.issue_date > datetime.date.today():
            raise ValidationError("issue date is not in future")

        super(Citizenship ,self).save(*args, **kwargs)

    
class Passport(BaseModel):
    student = models.OneToOneField(StudentModel,on_delete=CASCADE)
    passport_number = models.CharField(max_length=200,blank=True)
    issue_date = models.DateField(blank=True)
    expire_date = models.DateField(blank=True)
    issue_from = models.CharField(max_length=200,blank=True)
    passport_image=models.ImageField(
        upload_to = upload_student_identity_image_to,
        validators=[validate_image]
    )
    def save(self, *args ,**kwargs):
        if self.issue_date > datetime.date.today():
            raise ValidationError("issue date is not in future")

        if self.expire_date < datetime.date.today():
            raise ValidationError("expire date is not in past")

        super(Passport ,self).save(*args, **kwargs)
