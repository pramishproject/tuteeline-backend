from apps import consultancy
from apps.academic.models import Academic, PersonalEssay, StudentLor, StudentSop
from apps.studentIdentity.models import Citizenship, Passport
from apps.user.models import InstituteUser
from apps.consultancy.models import Consultancy, ConsultancyStaff
from apps.students.models import StudentAddress, StudentModel
from django.core import validators
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import models
from django.db.models import Q
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator,MinValueValidator
from apps.institute.models import Institute, InstituteScholorship, InstituteStaff
import datetime

from apps.core import fields
from apps.core.models import BaseModel
from apps.utils.currency import RealTimeCurrencyConverter

# Create your models here.

class Faculty(BaseModel):
    name = models.CharField(max_length=200)
    def __str__(self):
       return str(self.name)

class Course(BaseModel):
    faculty=models.ForeignKey(Faculty , on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    description=models.TextField()
    def __str__(self):
        return str(self.name)
    

class InstituteCourse(BaseModel):
    INTAKE_CHOICE=(
        ('spring' , 'spring'),
        ('yearly' , 'yearly'),
        ('fall' , 'fall' )
    )
    converter = RealTimeCurrencyConverter()
    CURRENCY=converter.CurrencyName()
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE ,related_name = 'course_related')
    program=models.CharField(max_length=200)
    faculty=models.ForeignKey(Faculty,on_delete=models.CASCADE)
    course= models.ForeignKey(Course,on_delete=models.CASCADE)
    intake=models.CharField(max_length=100,choices=INTAKE_CHOICE)
    #relete the eligibility exam in next table 
    eligibility = models.CharField(max_length=200)
    score = models.FloatField()  #this is eligibility score
    last_mini_academic_score = models.FloatField(
        validators=[MinValueValidator(40.0),MaxValueValidator(100.0)]
        )
    duration_year = models.IntegerField(
        validators=[MinValueValidator(1),MaxValueValidator(10)]
    ) 
    total_fee = models.DecimalField(max_digits=10, decimal_places=3)
    reg_fee = models.DecimalField(max_digits=10, decimal_places=3,blank=True,null=True)
    fee_currency = models.CharField(choices=CURRENCY,max_length=20)

    #this all are form open and close field

    reg_status = models.BooleanField(default=True)
    reg_open = models.DateField(
        _("Date"),
        blank=True
        )

    reg_close = models.DateField(
        _("Date"),
        blank=True
    )
    
    #required Document
    academic = models.BooleanField(default=False)
    citizenship = models.BooleanField(default=False)
    passport = models.BooleanField(default=False)
    essay = models.BooleanField(default=False)
    lor = models.BooleanField(default=False)
    sop = models.BooleanField(default=False)
    @property
    def get_course_name(self):
        return self.course.name

    @property
    def get_faculty_name(self):
        return self.faculty.name

    class Meta:
        unique_together = ('course','institute')




class InstituteApply(BaseModel):
    ACTION_OPTION=(
        ('verify','verify'),
        ('accept','accept'),
        ('reject','reject'),
        ('pending','pending'),
        ('applied','applied')
    )
    student = models.ForeignKey(StudentModel, 
    on_delete=DO_NOTHING
    )
    course = models.ForeignKey(InstituteCourse, on_delete=DO_NOTHING)
    consultancy = models.ForeignKey(
        Consultancy, 
        blank=True, 
        null=True,
        on_delete=DO_NOTHING
        )
    
    action = models.CharField(
        choices=ACTION_OPTION, 
        default='applied', 
        max_length=20
        )
    action_data = models.DateField(_('Date'), blank=True, null=True)
    institute = models.ForeignKey(Institute, on_delete=CASCADE)
    action_institute_user = models.ForeignKey(
        InstituteStaff, 
        blank=True, 
        null=True,
        on_delete=DO_NOTHING
        )
    action_consultancy_user = models.ForeignKey(
        ConsultancyStaff, 
        blank=True, 
        null=True, 
        on_delete=DO_NOTHING
        )
    view_date = models.DateField(blank=True, null=True)
    forward = models.BooleanField(default=False)
    cancel = models.BooleanField(default=False)

    @property
    def institute_data(self):
        return {
            "name":self.institute.name,
            "logo":self.institute.logo.path,
            "email":self.institute.institute_email,
            "contact":self.institute.contact,
            "country":self.institute.country,
        }

    @property
    def consultancy_data(self):
        if self.consultancy is not None:
            return {
                "name":self.consultancy.name,
                "logo":self.consultancy.logo.path,
                "email":self.consultancy.email,
                "contact":self.consultancy.contact,
            }
    @property
    def institute_user_action(self):
        return self.action_institute_user.user.fullname
    @property
    def get_student_user_name(self):
        return self.student.fullname

    @property
    def get_student_course(self):
        return self.course.course.name

    @property
    def get_faculty_name(self):
        return self.course.faculty

    @property
    def student_address(self):
        try:
            self.address = StudentAddress.objects.get(student=self.student)
            return self.address.country
        except StudentAddress.DoesNotExist:
            return None
    @property
    def get_consultancy_name(self):
        if self.consultancy != None:
            return self.consultancy.name
        else:
            return None

    class Meta:
        unique_together = ('student','course')

class AddScholorshipInCourse(BaseModel):
    course = models.ForeignKey(
        InstituteCourse,
        on_delete=DO_NOTHING
        )
    scholorship = models.ForeignKey(
        InstituteScholorship,
        on_delete=CASCADE
    )
    
    # pass

class CommentApplicationInstitute(BaseModel):
    application = models.ForeignKey(InstituteApply,on_delete=DO_NOTHING)
    institute_user = models.ForeignKey(InstituteStaff,on_delete=DO_NOTHING)
    comment = models.TextField()

    @property
    def commentor_name(self):
        return self.institute_user.user.fullname



class CommentApplicationConsultancy(BaseModel):
    application = models.ForeignKey(InstituteApply,on_delete=DO_NOTHING)
    consultancy_user = models.ForeignKey(ConsultancyStaff,on_delete=DO_NOTHING)
    comment = models.TextField()




class CheckedAcademicDocument(BaseModel):
    application = models.ForeignKey(InstituteApply,on_delete=CASCADE, related_name='checked_student_academic')
    academic = models.ForeignKey(Academic, on_delete=models.CASCADE)

    @property
    def get_academic_doc_name(self):
        return self.academic.name
    class Meta:
        unique_together = ('application','academic')

class CheckStudentIdentity(BaseModel):
    application = models.ForeignKey(InstituteApply,on_delete=CASCADE, related_name='checked_student_identity')
    citizenship=models.ForeignKey(Citizenship, on_delete=models.CASCADE,null=True,blank=True)
    passport = models.ForeignKey(Passport, on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        unique_together = ('application','citizenship')
#
class CheckedStudentLor(BaseModel):
    application = models.ForeignKey(InstituteApply,on_delete=CASCADE, related_name='checked_student_lor')
    lor = models.ForeignKey(StudentLor, on_delete=models.CASCADE)
    @property
    def get_lor_name(self):
        return self.lor.name


class CheckedStudentEssay(BaseModel):
    application = models.ForeignKey(InstituteApply, on_delete=CASCADE, related_name='checked_student_essay')
    essay = models.ForeignKey(PersonalEssay, on_delete=models.CASCADE)


class CheckedStudentSop(BaseModel):
    application = models.ForeignKey(InstituteApply, on_delete=CASCADE, related_name='checked_student_sop')
    sop = models.ForeignKey(StudentSop,on_delete=models.CASCADE)

    # @property
    # def get_sop_name(self):
    #     return self.sop.name
    class Meta:
        unique_together = ('application','sop')
