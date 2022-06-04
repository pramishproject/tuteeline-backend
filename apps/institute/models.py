from apps import institute
from datetime import datetime
from django.core import validators
from django.db.models import Q
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import models
from django.core.validators import validate_email

from apps.institute.utils import past_date,upload_institute_staff_image_to,upload_institute_logo_to,upload_institute_cover_image_to
from apps.core import fields
from apps.core.models import BaseModel
from apps.core.validators import validate_image
from apps.staff.models import StaffPosition
from apps.user.models import InstituteUser
from apps.institute.utils import upload_facility_image_to
from django.core.validators import MaxValueValidator,MinValueValidator
# from apps.institute_course.models import InstituteCourse


# Create your models here.
class Institute(BaseModel):
    TYPE_CHOICE=(
        ('PUBLIC','public'),
        ('PEIVATE','private')
    )
    name = models.CharField(max_length=250)
    contact = fields.PhoneNumberField()
    category = models.CharField(max_length=200)   #this represemt college or university
    university = models.CharField(max_length=200, blank=True) #if catagory is college then add university name else not required
    established = models.DateField(
        default=datetime.now,
        validators= [past_date]
         )
    institute_email = models.EmailField(blank = True,validators = [validate_email,])
    rating = models.FloatField(
        validators=[MinValueValidator(0.0),MaxValueValidator(5.0)], default=0.0
    )
    # email = models.EmailField(unique = True ,validators = [validate_email,])
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    street_address = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    website = models.URLField(blank=True,null=True)
    logo = models.ImageField(
        upload_to=upload_institute_logo_to,
        default='institute/logo/default_logo.png',
        validators=[validate_image]
    )
    cover_image = models.ImageField(
        upload_to=upload_institute_cover_image_to,
        default='institute/cover_image/default_cover_image.png',
        validators=[validate_image]
    )
    about = models.TextField(null=True, blank=True)
    type = models.TextField(max_length=200,choices=TYPE_CHOICE,blank=True,null=True)
    def __str__(self):
        return self.name
    @property
    def social_media(self):
        self._social_media = [{"name":social_media.name,"link":social_media.link} for social_media in SocialMediaLink.objects.filter(institute=self.id)]
        return self._social_media

class InstituteStaff(BaseModel):
    user = models.OneToOneField(InstituteUser, on_delete=models.CASCADE)
    institute = models.ForeignKey(Institute,on_delete=models.CASCADE)
    role = models.ForeignKey(StaffPosition, on_delete=models.CASCADE)
    profile_photo= models.ImageField(
        upload_to=upload_institute_staff_image_to,
        default="institute_staff/photo/default_logo.png",
        validators=[validate_image]
    )

    @property
    def get_institute_user_email(self):
        return self.user.email 

    @property
    def get_institute_full_name(self):
        return self.user.fullname

    @property
    def get_user_role(self):
        return self.role.name

    def __self__(self):
        return self.user.email 

    def clean(self):
        if self.role.name == 'owner' and StaffPosition.objects.filter(
            name__iexact='owner',
        ).exists():
            raise DjangoValidationError(
                {
                    'role':_('Cannot Assign two owners. ')
                }
            )


class RequiredDocument(BaseModel):
    photo = models.BooleanField()
    citizenship = models.BooleanField()
    passport = models.BooleanField()
    academic_certificate = models.BooleanField()
    sop = models.BooleanField()
    lor = models.BooleanField()



class InstituteScholorship(BaseModel):
    institute = models.ForeignKey(Institute,on_delete=CASCADE)
    topic = models.CharField(max_length=200)
    description = models.TextField()
    max_scholorship_percentage = models.FloatField(default=0.0)
    def __str__(self):
        return self.topic

class SocialMediaLink(BaseModel):
    SOCIAL_MEDIA = (
        ('facebook','facebook'),
        ('youtube','youtube'),
        ('linkdin','linkdin'),
        ('instagram','instagram')
    )
    institute  = models.ForeignKey(Institute,on_delete=CASCADE)
    name = models.CharField(choices=SOCIAL_MEDIA,max_length=100)
    link = models.URLField()

    class Meta:
        unique_together = ('institute','name')



class Facility(BaseModel):
    name = models.CharField(max_length=20)
    icon = models.FileField(upload_to=upload_facility_image_to)

    
    def __str__(self):
        return self.name


class AddInstituteFacility(BaseModel):
    facility = models.ForeignKey(Facility,on_delete=DO_NOTHING)
    institute = models.ForeignKey(Institute,on_delete=CASCADE ,related_name='facility_related')

    @property
    def get_facility_name(self):
        return self.facility.name

    @property
    def get_facility_icone(self):
        return self.facility.icon