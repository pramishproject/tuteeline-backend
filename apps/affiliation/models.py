from django.db import models
from apps.core.models import BaseModel
# Create your models here.
from apps.institute.models import Institute


class Affiliation(BaseModel):
    institute = models.ForeignKey(Institute,on_delete=models.CASCADE,related_name="institute_affiliation")
    university = models.ForeignKey(Institute,on_delete=models.CASCADE , related_name="university_affiliation")
    course = models.JSONField()# {type:"ALL or CUSTOM",course:["course_id"]}
    verify = models.BooleanField(default=False)
    class Meta:
        unique_together = ('institute','university')