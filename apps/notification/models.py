from apps.core.models import BaseModel
from django.db import models
from apps.institute.models import Institute
from apps.students.models import StudentModel
from django.contrib.auth import get_user_model

User = get_user_model()
class Notification(BaseModel):
    TO_USER=(
        ("INSTITUTE","INSTITUTE"),
        ("STUDENT","STUDENT"),
        ("STAFF","STAFF")
    )
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    institute = models.ForeignKey(to=Institute,on_delete=models.CASCADE)
    to=models.CharField(choices=TO_USER,max_length=100)
    message = models.CharField(max_length=300)
