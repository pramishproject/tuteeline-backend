from django.db.models.deletion import CASCADE, DO_NOTHING
from apps.institute.models import Institute
from django.db import models

# Create your models here.
from apps.blog.utils import upload_blog_image_to
from apps.core.models import BaseModel
from apps.core.validators import validate_image
from apps.portal.models import PortalStaff
from apps.user.models import InstituteUser


class Relation(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Blogs(BaseModel):
    relation = models.ForeignKey(to=Relation, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    author_name = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to=upload_blog_image_to,
                              default='consultancy/logo/default_logo.png',
                              validators=[validate_image]
                              )

    def __str__(self):
        return self.title


class InstituteBlog(BaseModel):
    institute = models.ForeignKey(to=Institute , on_delete= CASCADE)
    user = models.ForeignKey(InstituteUser, on_delete= models.SET_NULL, blank=True, null=True)
    relation = models.ForeignKey(to=Relation, on_delete=CASCADE)
    title = models.CharField(max_length=100)
    author_name = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to=upload_blog_image_to,
                              default='institute/blog/default_logo.png',
                              validators=[validate_image]
                              )
    verified = models.BooleanField(default=False)
    def __str__(self):
        return self.title


class PortalBlog(BaseModel):
    user= models.ForeignKey(to=PortalStaff, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    author_name = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to=upload_blog_image_to,
                              default='portel/blog/default_logo.png',
                              validators=[validate_image]
                              )
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class PortalBlogImage(models.Model):
    image = models.ImageField(upload_to=upload_blog_image_to,
                              default='institute/blog/default_logo.png',
                              validators=[validate_image]
                              )
