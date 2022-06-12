from django.db import models

# Create your models here.
from apps.consultancy.models import Consultancy, ConsultancyStaff
from apps.core.models import BaseModel
from apps.core.validators import validate_image
from apps.gallery.utils import upload_gallery_image_to
from apps.institute.models import Institute, InstituteStaff


class ConsultancyGallery(BaseModel):
    title = models.CharField(max_length=100)
    consultancy = models.ForeignKey(to=Consultancy,on_delete=models.CASCADE,blank=True,null=True)
    uploaded_image = models.ForeignKey(ConsultancyStaff, on_delete=models.DO_NOTHING)
    approve = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to=upload_gallery_image_to,
        default='consultancy/logo/default_logo.png',
        validators=[validate_image]
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'consultancy_galleries'


class InstituteGallery(BaseModel):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    uploaded_image = models.ForeignKey(InstituteStaff, on_delete=models.DO_NOTHING)
    approve = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to=upload_gallery_image_to,
        default='consultancy/logo/default_logo.png',
        validators=[validate_image]
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'institute_galleries'

    
