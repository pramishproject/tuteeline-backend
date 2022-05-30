from django.db import models

# Create your models here.
from apps.core.models import BaseModel
from apps.core.validators import validate_image
from apps.gallery.utils import upload_gallery_image_to
from apps.institute.models import Institute, InstituteStaff


class Gallery(BaseModel):
    title = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to=upload_gallery_image_to,
        default='consultancy/logo/default_logo.png',
        validators=[validate_image]
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'galleries'


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

    
