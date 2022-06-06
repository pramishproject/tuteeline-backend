from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from apps.core.models import BaseModel

User = get_user_model()


class Settings(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    color = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        default='#800000'
    )
    two_fa = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
