from django.db import models

from apps.consultancy.models import Consultancy
from apps.core.models import BaseModel
# Create your models here.
from apps.institute.models import Institute
from apps.linkage.utils import upload_linkage_docs

STATUS=(
    ('ACCEPT','accept'),
    ('REJECT','reject'),
)
class Linkage(BaseModel):
    institute = models.ForeignKey(to=Institute,on_delete=models.CASCADE)
    consultancy = models.ForeignKey(to=Consultancy,on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS,max_length=10)

    @property
    def get_consultancy_data(self):
        return {
            "name":self.consultancy.name,
            "logo":self.consultancy.logo.name,
            "email":self.consultancy.consultancy_email,
            "contact":self.consultancy.contact,
            "address": self.consultancy.country + "," +self.consultancy.state +"," + self.consultancy.city
        }

class LinkageDocs(BaseModel):
    linkage = models.ForeignKey(to=Linkage,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    document = models.FileField(upload_to=upload_linkage_docs)
