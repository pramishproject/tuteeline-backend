from django.db import models

from apps.core.models import BaseModel
# Create your models here.

class Activity(BaseModel):
    type = models.CharField(max_length=100)
    #this was choosen if the type is atheletic
    name = models.CharField(max_length=100,blank=True,null=True)
    position_leadership = models.CharField(max_length=100,blank=True,null=True)
    organization_name = models.CharField(max_length=100,blank=True,null=True)
    discription  = models.TextField()
