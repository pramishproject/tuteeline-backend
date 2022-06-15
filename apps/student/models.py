from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.college.models import College
from apps.college.search.models import PostManager
from apps.student.utils.file_function import (
    student_photo,
    validate_file,
    student_certificate,
    student_national_certificate
)
from apps.user.models import StudentUser

User = get_user_model()



class Student(models.Model):
    id = models.OneToOneField(
        StudentUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    contact = models.CharField(max_length=200)
    dob = models.DateField()
    gender = models.CharField(max_length=30, default="Male")
    country = models.CharField(max_length=100)
    street_name = models.CharField(max_length=100)
    city_town = models.CharField(max_length=200)
    state_provision = models.CharField(max_length=200)
    postal_code = models.IntegerField()
    apply = models.ManyToManyField(College, through='StudentApply')
    parents_isfull = models.BooleanField(default=False)
    photo = models.FileField(upload_to=student_photo, blank=True, validators=[validate_file])


class AcademicInfo(models.Model):
    class Meta:
        unique_together = (('student', 'level'),)

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Institute_name = models.CharField(max_length=200)
    duration = models.CharField(max_length=40, default="1")
    level = models.CharField(max_length=200)
    percentage = models.FloatField()
    outof = models.IntegerField(default=100)
    marksheet = models.FileField(upload_to=student_certificate)
    certificate = models.FileField(upload_to=student_certificate)


class Eligibility(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    eligibility_exam_name = models.CharField(max_length=600, null=True, blank=True)
    score = models.IntegerField()
    certificate = models.FileField(upload_to=student_certificate)


# class QueryForStudent(models.Model):
#     student=models.ForeignKey(Student, on_delete=models.CASCADE)
#     country=models.CharField(max_length=100)
#     University=models.CharField(max_length=100)
#     Course=models.CharField(max_length=100)
#     
STUDENT_ACTION = (
    ('1', 'no_action'),
    ('2', 'cancle'),
    ('3', 'denied'),
    ('4', 'Admit'),
)
COLLEGE_ACTION = (
    ('0', 'no_action'),
    ('1', 'accept'),
    ('2', 'reject'),
    ('3', 'hold'),

)


class StudentApply(models.Model):
    class Meta:
        unique_together = (('college', 'student'),)

    college = models.ForeignKey(College, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200, default="pramish")
    middle_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, default="karki")
    status = models.CharField(max_length=40, default='0')
    applyed = models.BooleanField()
    view_date = models.DateTimeField(default=timezone.now)
    action_date = models.DateTimeField(default=timezone.now)
    apply_date = models.DateTimeField(auto_now=True)
    view = models.BooleanField(default=False, blank=False)
    student_action = models.CharField(max_length=6, choices=STUDENT_ACTION, default='1')
    form_payment = models.BooleanField(default=False)
    enrolled = models.BooleanField(default=False)
    objects = PostManager()

    def __str__(self):
        return self.student_action


class Comment(models.Model):
    apply = models.ForeignKey(StudentApply, on_delete=models.CASCADE)
    comment = models.TextField()
    # date=models.DateTimeField(blank=True,default="")


class Bookmark(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)


class VisitedCollege(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)


class Parents(models.Model):
    class Meta:
        unique_together = (('relation', 'student'),)

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    parents_type = models.CharField(max_length=100)
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=200)
    occupation = models.CharField(max_length=100)
    education = models.CharField(max_length=200)
    relation = models.CharField(max_length=200, default="Father")


# class StudentTracker(models.Model):
#     cid=models.ForeignKey(College, on_delete=models.CASCADE)
#     sid=models.ForeignKey(Student, on_delete=models.CASCADE)
#     apply=models,
# class NationalIDs(models.Model):
#     id=models.OneToOneField(
#         Student,
#         on_delete=models.CASCADE,
#         primary_key=True,
#     )
#     citizenship=models.FileField(upload_to=student_certificate,blank=True)
#     passport=models.FileField(upload_to=student_certificate,blank=True)
class CitizenshipModel(models.Model):
    id = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    front_page = models.FileField(upload_to=student_national_certificate, blank=True)
    back_page = models.FileField(upload_to=student_national_certificate, blank=True)


class PassportModel(models.Model):
    id = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    passport = models.FileField(upload_to=student_national_certificate, blank=True)


class LORModel(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lor = models.FileField(upload_to=student_certificate, blank=True)


# class SOP(models.Model):
#     student=models.ForeignKey(Student, on_delete=models.CASCADE)
#     sop=models.TextField()
# class StudentSOP(models.Model):
#     student=models.ForeignKey(Student, on_delete=models.CASCADE)
#     title=models.CharField(max_length=50)
#     sop=models.FileField(upload_to=student_certificate,blank=True)
class StudentEssay(models.Model):
    id = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    topic = models.CharField(max_length=300)
    essay = models.TextField()
