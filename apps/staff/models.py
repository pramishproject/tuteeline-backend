from django.db import models

# Create your models here.
from apps.core.models import BaseModel


class StaffPosition(BaseModel):
    name = models.CharField(max_length=20)
    consultancy = models.ForeignKey('consultancy.Consultancy',
                                    blank=True, null=True,
                                    related_name="consultancy_staff_role",
                                    on_delete=models.CASCADE)
    institute = models.ForeignKey("institute.Institute",
                                  blank=True,
                                  null=True,
                                  related_name="institute_staff_role",
                                  on_delete=models.CASCADE)
    permission_list = models.JSONField(default=[])
    portal = models.BooleanField(default=False)
    # manager , true -> save
    # manager, false -> raise
    class Meta:
        default_permissions = ()

    def __str__(self):
        return self.name

    # def clean(self):
    #     super(StaffPosition).updated_at =self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(StaffPosition, self).save(*args, **kwargs)




INSTITUTE_PERMISSIONS = [
    "ACTION_INSTITUTE_APPLICATION",
    "VIEW_STUDENT_APPLICATION",
    "COMMENT_INSTITUTE_APPLICATION",
    "EDIT_INSTITUTE_PROFILE",
    "USER_MANAGEMENT",
    "ADD_DELETE_EDIT_INSTITUTE_GALLERY",
    "ADD_DELETE_EDIT_INSTITUTE_BLOGS",
    "COUNSELLING_INSTITUTE_STUDENT",
    "APPROVE_LINKAGE_REQUEST",
    "VIEW_LINKAGE_REQUEST",
    "VIEW_DASHBOARD",
    "ADD_EDIT_DELETE_AFFILIATION",
    "ADD_DELETE_EDIT_INSTITUTE_COURSE",

]

class RoleBase(BaseModel):
    institute = models.ForeignKey("institute.Institute",blank=True,null=True,related_name="institute_role",on_delete=models.CASCADE)
    consultancy = models.ForeignKey('consultancy.Consultancy', blank=True, null=True, related_name="consultancy_role", on_delete=models.CASCADE)
    portal = models.BooleanField(default=False)
    role_name = models.CharField(max_length=100)
    permission_list = models.JSONField()

    class Meta:
        unique_together = ('institute', 'consultancy','portal','role_name')

    def __str__(self):
        return self.role_name

    # def clean(self):
    #     super(StaffPosition).updated_at =self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(RoleBase, self).save(*args, **kwargs)
