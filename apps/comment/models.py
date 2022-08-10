

from django.db import models

from apps.comment.utils import upload_comment_image_to
from apps.core.models import BaseModel
# Create your models here.
from django.contrib.auth import get_user_model

from apps.institute.models import InstituteStaff
from apps.institute_course.models import InstituteApply
from apps.students.models import StudentModel
from apps.user.models import InstituteUser, StudentUser

User = get_user_model()
USER_TYPE_CHOICES = (
        ('portal_user', 'portal_user'),
        ('institute_user', 'institute_user'),
        ('consultancy_user', 'consultancy_user'),
        ('student_user', 'student_user'),
    )
class ApplicationComments(BaseModel):
    user_id = models.ForeignKey(to=User,on_delete=models.CASCADE)
    text_comment = models.TextField(
        blank=True,
        null=True
    )
    user_type = models.CharField(choices=USER_TYPE_CHOICES,max_length=100,blank=True,null=True)
    file_comment = models.FileField(
        upload_to=upload_comment_image_to,
        blank=True,
        null=True,)
    parent_comment = models.ForeignKey(to="ApplicationComments",on_delete=models.CASCADE,null=True,blank=True)
    application = models.ForeignKey(to=InstituteApply,on_delete=models.CASCADE)

    @property
    def user_data(self):
        if self.user_id.user_type=="institute_user":
            try:
                staff = InstituteStaff.objects.get(user=self.user_id)
                return {
                    "name":staff.user.fullname,
                    "profile": staff.profile_photo.url,
                    "organization": staff.institute.name
                }
            except InstituteStaff.DoesNotExist:
                return {
                    "name":"Anonymous",
                    "profile": None,
                    "organization": None
                }

        elif self.user_id.user_type == "student_user":
            try:
                student = StudentModel.objects.get(user = self.user_id)
                return {
                    "name":student.fullname,
                    "profile": student.image.url,
                    "organization": "student"
                }
            except StudentModel.DoesNotExist:
                return {
                    "name": "Anonymous",
                    "profile": None,
                    "organization": None
                }

        return {
            "name": "Anonymous",
            "profile": None,
            "organization": None
        }