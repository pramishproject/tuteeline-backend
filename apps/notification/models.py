from apps.core.models import BaseModel
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# class Notification(BaseModel):
#     send_to = models.ForeignKey(to=User,on_delete=models.CASCADE)
#     send_from = models.ForeignKey(to=User,on_delete=models.CASCADE)
#     message = models.CharField(max_length=300)
