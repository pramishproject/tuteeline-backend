from django.db.models.lookups import In
from apps import institute
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import models
from django.db.models import Q
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.utils.translation import gettext_lazy as _

from apps.students.utils import upload_student_image_to
from apps.core import fields
from apps.core.models import BaseModel
from apps.core.validators import validate_image
from apps.user.models import StudentUser
from apps.institute.models import Institute

class StudentModel(BaseModel):
    GENDER_CHOOSE=(
        ('male','male'),
        ('female','female'),
        ('others','others')
    )
    user = models.OneToOneField(StudentUser, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=250)
    contact = fields.PhoneNumberField()
    latitude = models.FloatField(blank=True)
    longitude = models.FloatField(blank=True)
    image = models.ImageField(
        upload_to=upload_student_image_to,
        default='student/image/default_logo.png',
        validators=[validate_image]
    )
    gender = models.CharField(
        choices=GENDER_CHOOSE,
        default="male",
        max_length=20
        )
    
    dob = models.DateField(blank=True, null=True)


    def __str__(self):
        return self.fullname




errors = {
    'unique':'address of the user already exist'
}

class StudentAddress(BaseModel):
    NATIONALITY_CHOOSE = (
        ('afghan','Afghan'),
        ('albanian','Albanian'),
        ('Algerian','Algerian'),
        ('Argentinian','Argentinian'),
        ('Australian','Australian'),
        ('Austrian','Austrian'),
        ('Bangladeshi','Bangladeshi'),
        ('Belgian','Belgian'),
        ('Bolivian','Bolivian'),
        ('Batswana','Batswana'),
        ('nepales','nepalies'),
        ('indian','indian'),
        
    )
    student = models.OneToOneField(
        StudentModel, 
        on_delete=models.CASCADE,
        error_messages=errors,
        related_name='address_relation'
        )
    nationality =models.CharField(
        choices=NATIONALITY_CHOOSE,
        default="nepales",
        max_length=20)
    state_provision = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=200)

    def __str__(self):
        return self.country


class CompleteProfileTracker(BaseModel):
    student = models.OneToOneField(StudentModel, on_delete=CASCADE,related_name='application_tracker')
    complete_address = models.BooleanField(default=False)
    complete_academic_detail = models.BooleanField(default=False)
    complete_parents_detail = models.BooleanField(default=False)
    complete_citizenship_detail = models.BooleanField(default=False)
    complete_passport_field= models.BooleanField(default=False)
    complete_sop_field = models.BooleanField(default=False)
    complete_personalessay_field = models.BooleanField(default=False)
    complete_lor_field = models.BooleanField(default=False)
    def __str__(self):
        return self.student.name


class FavouriteInstitute(BaseModel):
    student = models.ForeignKey(
        StudentModel,
        on_delete=DO_NOTHING
        )
    institute = models.ForeignKey(
        Institute,
        on_delete=DO_NOTHING
    )
    class Meta:
        unique_together = ['student','institute']


class InstituteViewers(BaseModel):
    student = models.ForeignKey(StudentModel,on_delete=CASCADE)
    institute = models.ForeignKey(Institute, on_delete=CASCADE)
    class Meta:
        unique_together = ['student','institute']