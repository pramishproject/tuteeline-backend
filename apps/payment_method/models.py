from django.db import models
from apps.core.models import BaseModel
# Create your models here.
from apps.institute.models import Institute


class PaymentMethod(BaseModel):
    institute = models.ForeignKey(to=Institute,on_delete=models.CASCADE)
    cash_receipt = models.BooleanField(default=False)
    esewa = models.BooleanField(default=False)
    khalti = models.BooleanField(default=False)
    skrill = models.BooleanField(default=False)
    stripe = models.BooleanField(default=False)
    paypal = models.BooleanField(default=False)
    payment_detail = models.JSONField()
        #     {
        #     "esewa":{
        #       "esewa_id":""
        #     },
        #       "khalti":{
        #           "khalti_id":""
        # },
        #    "cash_recipt":{
        #    "account_no":"",
        #    "branch":"branch",
        #    "name":"",
        #    }
        #     }
