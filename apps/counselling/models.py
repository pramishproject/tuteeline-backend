from django.db import models
from apps.core.models import BaseModel
from apps.students.models import StudentModel
from apps.institute.models import Institute,InstituteStaff
from apps.academic.models import LEVEL_CHOICE
from apps.institute_course.models import InstituteCourse
# Create your models here.

COUNCELLING_STATUS = (
    ("START","start"),
    ("COMPLETE","complete"),
    ("NOT STARTED","not_start")
)
class InstituteCounselling(BaseModel):
    student = models.ForeignKey(to=StudentModel,on_delete=models.CASCADE)
    institute = models.ForeignKey(to=Institute,on_delete=models.CASCADE)
    education_level = models.CharField(choices=LEVEL_CHOICE,max_length=200)
    which_time = models.DateTimeField(blank=True)
    physical_counelling = models.BooleanField(default=True)
    assign_to = models.ForeignKey(to=InstituteStaff,on_delete=models.DO_NOTHING,blank=True,null=True)
    status = models.CharField(max_length=100,choices=COUNCELLING_STATUS,default="not_start")
    notes = models.TextField(default="",blank=True,null=True)
    class Meta:
        unique_together= ("student","institute")

class InterestedCourse(BaseModel):
    counselling = models.ForeignKey(to=InstituteCounselling,on_delete=models.CASCADE)
    course = models.ForeignKey(to=InstituteCourse,on_delete=models.CASCADE)
    class Meta:
        unique_together=("counselling","course")


