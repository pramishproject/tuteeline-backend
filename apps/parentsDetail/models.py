from django.core import validators
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import models
from django.db.models import Q
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxLengthValidator, MaxValueValidator,MinLengthValidator

from apps.core import fields
from apps.core.models import BaseModel
from apps.students.models import StudentModel

class StudentParents(BaseModel):
    RELATION_CHOICE = (
        ('father','father'),
        ('mother','mother'),
        ('limited_information','limited_information')
    )
    student = models.ForeignKey(StudentModel , on_delete=CASCADE,related_name="parents")
    relation = models.CharField(choices=RELATION_CHOICE,max_length=20)
    fullname = models.CharField(max_length=200)
    email = models.EmailField(blank=True,null=True)
    country_code = models.CharField(max_length=20,blank=True,null=True)
    contact = models.CharField(max_length=20,blank=True)
    nationality = models.CharField(max_length=200)
    occupation = models.CharField(max_length=200)
    education = models.CharField(max_length=200)
    annual_income = models.FloatField(blank=True,default=0.0) #defauly should be in dollor
    currency = models.CharField(default="USD",max_length=50)

    class Meta:
        unique_together = ('student','relation')

class HouseHold(BaseModel):
    MARITIAL_STATUS= (
        ('never_married','never_married'),
        ('seperated','seperated'),
        ('divorced','divorced'),
        ('widowed','widowed'),
        ('domestic_parents','domestic_parents')
    )
    student = models.ForeignKey(StudentModel , on_delete=CASCADE)
    maritial_status =  models.CharField(choices=MARITIAL_STATUS,max_length=100)
    children = models.BooleanField(default=False)
    no_of_childrents = models.IntegerField(
        blank=True,
        validators = [
            MaxValueValidator(10),
            MinLengthValidator(0)
        ])

class Siblings(BaseModel):
    student = models.ForeignKey(StudentModel , on_delete=CASCADE)
    full_name = models.CharField(max_length=100)
    age = models.IntegerField(
        validators = [
            MaxValueValidator(100),
            MinLengthValidator(1)
        ])
    