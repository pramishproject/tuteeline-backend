from django.db import models

from .search.models import PostManager
from ..student.utils.file_function import content_file_name, pdfformat, content_Gallery_name, validate_file
from ..user.models import InstituteUser


class Faculty(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    objects = PostManager()

    def __str__(self):
        return self.name


class Facility(models.Model):
    facility = models.CharField(max_length=200)


class College(models.Model):
    id = models.OneToOneField(
        InstituteUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    category = models.CharField(max_length=200)
    university = models.CharField(max_length=200, blank=True)
    established = models.CharField(max_length=200)
    logourl = models.FileField(upload_to=content_file_name)
    coverpage = models.FileField(upload_to=content_file_name)
    brochure = models.FileField(upload_to=content_file_name, validators=[pdfformat], blank=True)
    country = models.CharField(max_length=200)
    location = models.CharField(max_length=300, blank=True)
    facility = models.ManyToManyField(Facility)
    lat = models.FloatField()
    long = models.FloatField()
    about = models.TextField(blank=True)
    type = models.CharField(max_length=200, default="private")
    schlorship = models.BooleanField(default=True)
    website = models.URLField(blank=True)
    review = models.FloatField(default=1.1)
    select_restricted_country = models.BooleanField(default=False)
    add_course = models.BooleanField(default=False)
    male_student = models.IntegerField(default=0)
    femail_student = models.IntegerField(default=0)
    professor = models.IntegerField(default=0)
    teacher = models.IntegerField(default=0)
    staff = models.IntegerField(default=0)
    approved_by = models.CharField(max_length=200, default="UGC")
    dashboard_custom_color = models.CharField(max_length=20)
    light_mode = models.BooleanField(default=True)
    area = models.CharField(max_length=200, blank=True, default="")
    climate_description = models.CharField(max_length=500, blank=True, default="")
    # opening_time=models.TimeField(blank=True)
    # closing_time=models.TimeField(blank=True)
    objects = PostManager()

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CourceDetail(models.Model):
    class Meta:
        unique_together = (('college', 'course'),)

    course = models.CharField(max_length=200)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    faculty = models.CharField(max_length=200)
    program = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    eligibility_exam = models.CharField(max_length=200)
    score = models.FloatField()
    min_gpa = models.FloatField()
    Duration = models.CharField(max_length=100)
    Intake = models.CharField(max_length=100)
    fee = models.IntegerField()
    feeCurrency = models.CharField(max_length=100)
    seat = models.IntegerField(blank=True, default=10)
    photo = models.BooleanField(default=False)
    citizenship = models.BooleanField(default=False)
    passport = models.BooleanField(default=False)
    school_certificate = models.BooleanField(default=False)
    highschool_certificate = models.BooleanField(default=False)
    undergraduate_certificate = models.BooleanField(default=False)
    graduate_certificate = models.BooleanField(default=False)
    tor = models.BooleanField(default=False)
    sop = models.BooleanField(default=False)
    scholorship_scheme = models.TextField(default="")
    form_fee = models.FloatField(default=0)
    form = models.BooleanField(default=False)
    openDate = models.DateField(blank=True, null=True)
    closeDate = models.DateField(blank=True, null=True)


class CounselorModel(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200)
    photo = models.FileField(upload_to=content_file_name)
    contact = models.CharField(max_length=200)
    email = models.EmailField()
    description = models.TextField()
    responsibility = models.TextField()
    # entry_time=models.TimeField(blank=True)
    # exist_time=models.TimeField(blank=True)


ACCOMODATION = (
    ('single', 'SINGLE'),
    ('sharing', 'SHARING')
)
KITCHEN = (
    ('single', 'SINGLE'),
    ('sharing', 'SHARING'),
    ('Common Shaired Kitchen', 'COMMONSHAIREDKITCHEN')
)


class Accomodation(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    building = models.CharField(max_length=40)
    floor = models.CharField(max_length=20)
    room_no = models.CharField(max_length=20)
    room_type = models.CharField(max_length=200, choices=ACCOMODATION)
    kitchen = models.CharField(max_length=200, choices=KITCHEN)
    laundry = models.BooleanField()
    internet = models.BooleanField()
    attach_rest_room = models.BooleanField()
    fan = models.BooleanField()
    air_condition = models.BooleanField()
    swimming_pool = models.BooleanField()
    # no_staff=models.IntegerField()


# class AccomodationPicture(models.Model):
#     accomodation=models.ForeignKey(Accomodation, on_delete=models.CASCADE)
#     picture=models.FileField(upload_to=content_file_name)
HYGIENE = (
    ('poor', 'POOR'),
    ('good', 'GOOD'),
    ('very good', 'VERYGOOD'),
    ('excellent', 'EXCELLENT')
)


class Canteen(models.Model):
    college = models.OneToOneField(College,
                                   on_delete=models.CASCADE,
                                   primary_key=True, )
    building = models.CharField(max_length=40)
    floor = models.CharField(max_length=20)
    area = models.CharField(max_length=200)
    student_capacity = models.CharField(max_length=30)
    no_staff = models.CharField(max_length=40)
    hygiene = models.CharField(max_length=40, choices=HYGIENE)
    air_condition = models.BooleanField()
    fan = models.BooleanField()
    wash_room = models.BooleanField()
    wifi = models.BooleanField()
    drinking_water = models.BooleanField()


# class CantinPicture(models.Model):
#     cantin=models.ForeignKey(Canteen,on_delete=models.CASCADE)
#     picture=models.FileField(upload_to=content_file_name)


LABSAFTY = (
    ('poor', 'POOR'),
    ('good', 'GOOD'),
    ('very good', 'VERYGOOD'),
    ('excellent', 'EXCELLENT')
)


class Laboratory(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    lab_type = models.CharField(max_length=200)
    building = models.CharField(max_length=100)
    floor = models.CharField(max_length=200, blank=True)
    room = models.CharField(max_length=200, blank=True)
    student_capacity = models.CharField(max_length=200)
    opening_time = models.TimeField(blank=True)
    closing_time = models.TimeField(blank=True)
    description = models.TextField()
    no_staff = models.IntegerField()
    safety = models.CharField(max_length=200, choices=LABSAFTY)


# class LaboratoryPicture(models.Model):
#     labortatory=models.ForeignKey(Laboratory,on_delete=models.CASCADE)
#     picture=models.FileField(upload_to=content_file_name)

class LibraryModel(models.Model):
    college = models.OneToOneField(College,
                                   on_delete=models.CASCADE,
                                   primary_key=True, )
    building_no = models.CharField(max_length=100)
    floor_no = models.CharField(max_length=100)
    room_no = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    no_books = models.IntegerField()
    reading_room = models.BooleanField()
    description = models.TextField()


# class LibraryPicture(models.Model):

class Gallery(models.Model):
    status = models.CharField(max_length=100, blank=True)
    picture = models.FileField(upload_to=content_Gallery_name, validators=[validate_file])
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)


class StanderedRating(models.Model):
    college = models.OneToOneField(InstituteUser,
                                   on_delete=models.CASCADE,
                                   primary_key=True)
    country_rank = models.FileField()
    world_rank = models.FileField()
    international_student = models.IntegerField()
    m_f_ratio = models.FloatField()
    students = models.IntegerField()
    no_of_student_per_staff = models.FloatField()


class RestrictCountry(models.Model):
    class Meta:
        unique_together = (('cid', 'country'),)

    cid = models.ForeignKey(College, on_delete=models.CASCADE)
    country = models.CharField(max_length=200)


relation = (
    ('student', 'STUDENT'),
    ('employee', 'EMPLOYEE'),
    ('guest', 'GUEST')
)


class Blog(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    auther = models.CharField(max_length=100)
    institute_relation = models.CharField(max_length=100, choices=relation)
    work_on = models.CharField(max_length=300)
    post = models.CharField(max_length=200)
    publish = models.DateField()
    image = models.FileField(upload_to=content_file_name)
    heading = models.CharField(max_length=200)
    content = models.TextField()
