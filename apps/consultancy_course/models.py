from django.db import models

from apps.consultancy.models import Consultancy
from apps.core.models import BaseModel
# Create your models here.
from apps.utils.currency import RealTimeCurrencyConverter

converter = RealTimeCurrencyConverter()
CURRENCY = converter.CurrencyName()
class ConsultancyCourse(BaseModel):
    consultancy = models.ForeignKey(to=Consultancy,on_delete=models.CASCADE,related_name="consultancy_course")
    course = models.CharField(max_length=100)
    fee = models.FloatField()
    currency = models.CharField(choices=CURRENCY,max_length=100)
    course_description = models.TextField()
