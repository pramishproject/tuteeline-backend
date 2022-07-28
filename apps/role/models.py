from django.db import models

from apps.consultancy.models import Consultancy
from apps.core.models import BaseModel
# Create your models here.
from apps.institute.models import Institute


INSTITUTE_PERMISSIONS = [
    "ACTION_INSTITUTE_APPLICATION",
    "COMMENT_INSTITUTE_APPLICATION",
    "EDIT_INSTITUTE_PROFILE",
    "ADD_INSTITUTE_USER",
    "DELETE_INSTITUTE_USER",
    "EDIT_INSTITUTE_USER"
    "ADD_INSTITUTE_GALLERY",
    "DELETE_INSTITUTE_GALLERY",
    "ADD_INSTITUTE_BLOGS",
    "EDIT_INSTITUTE_BLOGS",
    "DELETE_INSTITUTE_BLOGS",
    "COUNSELLING_INSTITUTE_STUDENT",
    "APPROVE_LINKAGE_REQUEST",
    "VIEW_LINKAGE_REQUEST",
    "VIEW_DASHBOARD",
    "ADD_AFFILIATION",
    "EDIT_AFFILIATION",
    "DELETE_AFFILIATION",
    "ADD_INSTITUTE_COURSE",
    "DELETE_INSTITUTE_COURSE",
    "UPDATE_INSTITUTE_COURSE",
]

class Role(BaseModel):
    institute = models.ForeignKey(Institute,blank=True,null=True,related_name="institute_role",on_delete=models.CASCADE)
    consultancy = models.ForeignKey(Consultancy , blank=True,null=True,related_name="consultancy_role",on_delete=models.CASCADE)
    portal = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    permissions = models.JSONField()

    class Meta:
        unique_together = ('institute', 'consultancy','portal','name')
        db_table = "staff_role"

