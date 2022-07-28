from django.db import models

from apps.consultancy.models import Consultancy
from apps.core.models import BaseModel
# Create your models here.
from apps.institute.models import Institute


INSTITUTE_PERMISSIONS = [
    "ACTION_INSTITUTE_APPLICATION",
    "VIEW_STUDENT_APPLICATION",
    "COMMENT_INSTITUTE_APPLICATION",
    "EDIT_INSTITUTE_PROFILE",
    "ADD_DELETE_EDIT_INSTITUTE_USER",
    "VIEW_INSTITUTE_USER",
    "ADD_DELETE_EDIT_INSTITUTE_GALLERY",
    "ADD_DELETE_EDIT_INSTITUTE_BLOGS",
    "COUNSELLING_INSTITUTE_STUDENT",
    "APPROVE_LINKAGE_REQUEST",
    "VIEW_LINKAGE_REQUEST",
    "VIEW_DASHBOARD",
    "ADD_EDIT_DELETE_AFFILIATION",
    "ADD_DELETE_EDIT_INSTITUTE_COURSE",
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

    def __str__(self):
        return self.name

    # def clean(self):
    #     super(StaffPosition).updated_at =self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Role, self).save(*args, **kwargs)

