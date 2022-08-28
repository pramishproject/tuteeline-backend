from django.db import models
from apps.core.models import BaseModel
# Create your models here.
from apps.institute.models import Institute

from apps.payment_method.utils import upload_voucher_icon
from apps.students.models import StudentModel

PROVIDER_NAME=(
    ("KHALTI","KHALTI"),
    ("ESEWA","ESEWA")
)

PAYMENT_TYPE = (
    ("REGISTRATION_FEE","REGISTRATION_FEE"),
)
PAYMENT_METHOD = (
    ("KHALTI","KHALTI"),
    ("ESEWA","ESEWA"),
    ("CASH","CASH"),
)

class ProviderName(BaseModel):
    icon = models.FileField(upload_to=upload_voucher_icon)
    name = models.CharField(choices=PROVIDER_NAME,max_length=200)

class Provider(BaseModel):
    institute = models.ForeignKey(to=Institute, on_delete=models.CASCADE)
    provider_name = models.ForeignKey(to=ProviderName, on_delete=models.CASCADE,null=True,blank=True)
    provider_id = models.CharField(max_length=200)

    @property
    def get_provider_name(self):
        if self.provider_name != None:
            return {
                    "name":self.provider_name.name,
                    "icon":self.provider_name.icon.url,
                }
        else:
            return {}

class VoucherPayment(BaseModel):
    institute = models.ForeignKey(to=Institute, on_delete=models.CASCADE)
    account_no = models.CharField(max_length=200)
    branch = models.CharField(max_length=300)
    account_name = models.CharField(max_length=300)
    bank_name = models.CharField(max_length=200)

class Transaction(BaseModel):
    student = models.ForeignKey(to=StudentModel,on_delete=models.DO_NOTHING,blank=True,null=True)
    institute = models.ForeignKey(to=Institute,on_delete=models.DO_NOTHING,blank=True,null=True)
    payment_method = models.CharField(choices=PAYMENT_METHOD,max_length=100)
    payment_type = models.CharField(choices=PAYMENT_TYPE,max_length=200,blank=True,null=True)
    data = models.TextField(blank=True,null=True)
    json_data = models.JSONField(blank=True,null=True)
    amount  = models.FloatField()
    transaction_id = models.CharField(max_length=200,default="")
