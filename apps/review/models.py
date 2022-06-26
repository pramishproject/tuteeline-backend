from django.db import models

from apps.consultancy.models import Consultancy
from apps.core.models import BaseModel
from django.db.models.deletion import CASCADE
from apps.institute.models import Institute
from django.core.validators import MaxValueValidator,MinValueValidator
from apps.students.models import StudentModel
# Create your models here.

class InstituteReview(BaseModel):
    student = models.ForeignKey(StudentModel,on_delete=models.DO_NOTHING)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    review = models.TextField(blank=True)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0),MaxValueValidator(5.0)]
    )

    class Meta:
        unique_together= ('student','institute')

class ConsultancyReview(BaseModel):
    student = models.ForeignKey(StudentModel, on_delete=models.DO_NOTHING)
    consultancy = models.ForeignKey(Consultancy, on_delete=models.CASCADE)
    review = models.TextField(blank=True)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    class Meta:
        unique_together = ('student', 'consultancy')