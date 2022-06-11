from django.db import models

from apps.consultancy.models import Consultancy
from apps.core.models import BaseModel
# Create your models here.
from apps.institute.models import Institute

STATUS=(
    ('ACCEPT','accept'),
    ('REJECT','reject'),
)
class Linkage(BaseModel):
    institute = models.ForeignKey(to=Institute,on_delete=models.CASCADE)
    consultancy = models.ForeignKey(to=Consultancy,on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS,max_length=10)
    document = models.FileField()
