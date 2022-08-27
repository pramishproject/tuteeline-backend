from django.db import models
from apps.core.models import BaseModel
# Create your models here.
from apps.institute.models import Institute


# class PaymentMethod(BaseModel):
#     institute = models.ForeignKey(to=Institute,on_delete=models.CASCADE)
#     cash_receipt = models.BooleanField(default=False)
#     esewa = models.BooleanField(default=False)
#     khalti = models.BooleanField(default=False)
#     skrill = models.BooleanField(default=False)
#     stripe = models.BooleanField(default=False)
#     paypal = models.BooleanField(default=False)
#     payment_detail = models.JSONField()
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
from apps.payment_method.utils import upload_voucher_icon
from apps.students.models import StudentModel

PROVIDER_NAME=(
    ("KHALTI","KHALTI"),
    ("ESEWA","ESEWA")
)

PAYMENT_METHOD = (
    ("KHALTI","KHALTI"),
    ("ESEWA","ESEWA"),
    ("CASH","CASH"),
)

class ProviderName(BaseModel):
    icon = models.FileField(upload_to=upload_voucher_icon)
    name = models.CharField(max_length=200,choices=PROVIDER_NAME)

class Provider(BaseModel):
    institute = models.ForeignKey(to=Institute, on_delete=models.CASCADE)
    provider_name = models.ForeignKey(to=ProviderName, on_delete=models.CASCADE,null=True,blank=True)
    provider_id = models.CharField(max_length=200)

    @property
    def provider_name(self):
        if self.provider_name != None:
            return {
                    # "name":self.provider_name.name,
                    # "icon":self.provider_name.icon,
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
    data = models.TextField(blank=True,null=True)
    amount  = models.FloatField()
    transaction_id = models.CharField(max_length=200,default="")
