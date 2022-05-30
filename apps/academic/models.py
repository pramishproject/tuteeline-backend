from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import models
from django.db.models import Q
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator ,MinValueValidator
from rest_framework.validators import UniqueValidator
import os
from apps.core import fields
from apps.core.models import BaseModel
from apps.core.validators import validate_image
from apps.students.models import StudentModel
from django.db.models.signals import pre_save
from apps.academic.utils import check_score,upload_academic_doc_to

class Academic(BaseModel):
    LEVEL_CHOICE=(
        ('school','school'),
        ('high_school','high_school'),
        ('undergraduate','undergraduate'),
        ('graduate','graduate'),
        ('post_graduate','post_graduate')
    )
    student = models.ForeignKey(StudentModel ,on_delete=CASCADE)
    institute_name = models.CharField(max_length=200)
    duration = models.FloatField(
        validators=[MinValueValidator(0.0),MaxValueValidator(15.0)],
        blank=True
    )
    level = models.CharField(max_length=200,choices=LEVEL_CHOICE)
    score = models.FloatField()
    full_score=models.FloatField(
        validators=[MinValueValidator(0.0),MaxValueValidator(100.0)],
    )
    marksheet = models.FileField(
        upload_to=upload_academic_doc_to,
    )
    name =  models.CharField(max_length=100,default="Academic Document")
    certificate = models.FileField(
        upload_to=upload_academic_doc_to,
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student','level'],name='student academic')
        ]

class StudentSop(BaseModel):
    name= models.CharField(max_length=100,blank=True,null=True)
    student= models.ForeignKey(StudentModel, on_delete=CASCADE)
    document = models.FileField(
        upload_to=upload_academic_doc_to
    )
    doc_type = models.CharField(max_length=100,blank=True,null=True)
    def save(self,*args,**kwargs):
        name ,extension = os.path.splitext(str(self.document))
        self.doc_type = extension
        super(StudentSop, self).save(*args, **kwargs)

class StudentLor(BaseModel):
    name= models.CharField(max_length=100,blank=True,null=True)
    student = models.ForeignKey(StudentModel,on_delete=CASCADE)
    document = models.FileField(
        upload_to=upload_academic_doc_to
    )
    doc_type = models.CharField(max_length=100,blank=True,null=True)
    def save(self,*args,**kwargs):
        name ,extension = os.path.splitext(str(self.document))
        self.doc_type = extension
        super(StudentLor, self).save(*args, **kwargs)
class PersonalEssay(BaseModel):
    name= models.CharField(max_length=100,blank=True,null=True)
    student = models.ForeignKey(StudentModel,on_delete=CASCADE)
    essay = models.FileField(
        upload_to=upload_academic_doc_to,
        blank=True,
        null=True
    )
    content = models.TextField(blank=True,null=True)
    doc_type = models.CharField(max_length=100,blank=True,null=True)
    def save(self,*args,**kwargs):
        if self.essay != None:
            name ,extension = os.path.splitext(str(self.essay))
            self.doc_type = extension
            super(PersonalEssay, self).save(*args, **kwargs)

        
pre_save.connect(check_score, sender=Academic)
