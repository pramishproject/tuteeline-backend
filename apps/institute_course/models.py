from apps import consultancy
from apps.academic.models import Academic, PersonalEssay, StudentLor, StudentSop, LEVEL_CHOICE
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

COURSE_MODE = (
    ('full_time','full_time'),
    ('part_time','part_time'),
    ('both','both'),
)
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
    eligibility = models.CharField(max_length=200) #make it json with score todo
    score = models.FloatField()  #this is eligibility score
    no_of_seats = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(8000)],blank=True,null=True)
    last_mini_academic_score = models.FloatField(
        validators=[MinValueValidator(40.0),MaxValueValidator(100.0)]
        )
    duration_year = models.IntegerField(
        validators=[MinValueValidator(1),MaxValueValidator(10)]
    ) 
    total_fee = models.DecimalField(max_digits=10, decimal_places=3)
    reg_fee = models.DecimalField(max_digits=10, decimal_places=3,blank=True,null=True)
    fee_currency = models.CharField(choices=CURRENCY,max_length=20)
    qualification = models.CharField(choices=LEVEL_CHOICE,default="",max_length=100,null=True,blank=True)
    #this all are form open and close field
    # curriculum = models.TextField(default='')

    mode = models.CharField(choices=COURSE_MODE,default="",max_length=100)
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
    def get_course_data(self):
        return {
            "name":self.course.name,
            "description":self.course.description
        }
    @property
    def get_faculty_name(self):
        return self.faculty.name

    class Meta:
        unique_together = ('course','institute')



ACTION_OPTION=(
        ('verify','verify'),
        ('accept','accept'),
        ('reject','reject'),
        ('pending','pending'),
        ('applied','applied')
    )

ACTION_OPTION_CONSULTANCY = (
    ('verify','verify'),
    ('not_verify','not_verify')
)
class InstituteApply(BaseModel):

    student = models.ForeignKey(StudentModel, 
    on_delete=DO_NOTHING
    )
    course = models.ForeignKey(InstituteCourse, on_delete=models.CASCADE)
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
    action_field = models.ForeignKey('ApplyAction', blank=True, null=True,on_delete=models.DO_NOTHING,
                                     related_name="action_institute")
    consultancy_action = models.ForeignKey('ActionApplyByConsultancy',blank=True, null=True,on_delete=models.DO_NOTHING
                                           ,related_name="action_consultancy")
    institute = models.ForeignKey(Institute, on_delete=CASCADE,related_name="apply_institute")
    institute_staff_assign = models.ForeignKey(InstituteStaff,
                                               on_delete=models.CASCADE,
                                               blank=True,
                                               null=True,
                                               )
    view_date = models.DateField(blank=True, null=True)
    forward = models.BooleanField(default=False)
    cancel = models.BooleanField(default=False)
    request_for_application_fee = models.BooleanField(default=False)

    # university = models.ForeignKey(Institute, on_delete=models.DO_NOTHING,null=True,blank=True,related_name="university_forward")
    @property
    def institute_data(self):
        return {
            "name":self.institute.name,
            "logo":self.institute.logo.url,
            "email":self.institute.institute_email,
            "contact":self.institute.contact,
            "country":self.institute.country,
        }
    @property
    def assign_institute_staff(self):
        if self.institute_staff_assign != None:
            return {
                "name":self.institute_staff_assign.user.fullname,
                "id":self.institute_staff_assign.id,
                "email": self.institute_staff_assign.user.email,
                "contact": self.institute_staff_assign.contact,
            }
        return {}
    @property
    def consultancy_data(self):
        if self.consultancy is not None:
            return {
                "name":self.consultancy.name,
                "logo":self.consultancy.logo.url,
                "email":self.consultancy.consultancy_email,
                "contact":self.consultancy.contact,
            }

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
        parmanent = ""
        temporary = ""
        try:
            self.address = StudentAddress.objects.filter(student=self.student)
            # ('permanent', 'PERMANENT'),
            # ('temporary'
            for i in self.address:
                if i.type == "permanent":
                    parmanent = i.country+','+i.city +","+i.street +","+i.state_provision+","+str(i.postal_code)

                if i.type == "temporary":
                    temporary = i.country+','+i.city +","+i.street +","+i.state_provision+","+str(i.postal_code)
            data = {
                "permanent_address":parmanent,
                "temporary_address":temporary,
            }
            return data
        except StudentAddress.DoesNotExist:
            data = {
                "permanent_address": parmanent,
                "temporary_address": temporary,
            }
            return data
    @property
    def get_consultancy_name(self):
        if self.consultancy != None:
            return self.consultancy.name
        else:
            return None
    @property
    def get_institute_name(self):
        return self.institute.name
    class Meta:
        unique_together = ('student','course')

# class PaymentVerification(BaseModel):
#     apply = models.ForeignKey(to=InstituteApply,on_delete=models.DO_NOTHING)
#     institute_user = models.ForeignKey(to=InstituteStaff, on_delete=models.DO_NOTHING)
#     verify = models.BooleanField(default=False)

class ApplyAction(BaseModel):
    apply = models.ForeignKey(to=InstituteApply,on_delete=models.CASCADE)
    action = models.CharField(choices=ACTION_OPTION,
        default='applied',
        max_length=20)
    institute_user = models.ForeignKey(to=InstituteStaff,on_delete=models.DO_NOTHING,blank=True,null=True)

    @property
    def institute_user_detail(self):
        if self.institute_user != None:
            return {
                "name":self.institute_user.user.fullname,
                "profile_image" : self.institute_user.profile_photo.url,
                "role":self.institute_user.role.name
            }
        else:
            return {}

class ActionApplyByConsultancy(BaseModel):
    apply = models.ForeignKey(to=InstituteApply, on_delete=models.CASCADE)
    action = models.CharField(choices=ACTION_OPTION_CONSULTANCY,
                              default='applied',
                              max_length=20)
    consultancy_user = models.ForeignKey(to=ConsultancyStaff, on_delete=models.DO_NOTHING, blank=True, null=True)
    class Meta:
        db_table="consultancy_action"

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
    application = models.ForeignKey(InstituteApply,on_delete=models.CASCADE)
    institute_user = models.ForeignKey(InstituteStaff,on_delete=DO_NOTHING)
    comment = models.TextField()

    @property
    def commentor_name(self):
        return {"name":self.institute_user.user.fullname,
                "image":self.institute_user.profile_photo.url
                }



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
    @property
    def get_academic_data(self):
        return {
            "institute_name":self.academic.institute_name,
            "duration":self.academic.duration,
            "level":self.academic.level,
            "score":self.academic.score,
            "percentage":float((self.academic.score/self.academic.full_score)*100),
            "marksheet":self.academic.marksheet.url,
            "certificate":self.academic.certificate.url,

        }


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

    @property
    def get_lor_data(self):
        return {
            "name":self.lor.name,
            "lor":self.lor.document.url,
            "doc_type":self.lor.doc_type
        }


class CheckedStudentEssay(BaseModel):
    application = models.ForeignKey(InstituteApply, on_delete=CASCADE, related_name='checked_student_essay')
    essay = models.ForeignKey(PersonalEssay, on_delete=models.CASCADE)
    @property
    def get_essay_name(self):
        return self.essay.name

    @property
    def get_essay_data(self):
        return {
            "name":self.essay.name,
            "content":self.essay.content,
            "essay":self.essay.essay.url,
            "type":self.essay.doc_type
        }

class CheckedStudentSop(BaseModel):
    application = models.ForeignKey(InstituteApply, on_delete=CASCADE, related_name='checked_student_sop')
    sop = models.ForeignKey(StudentSop,on_delete=models.CASCADE)

    @property
    def get_sop_name(self):
        return self.sop.name

    @property
    def get_sop_data(self):
        return {
            "name":self.sop.name,
            "document":self.sop.document.url,
            "doc_type":self.sop.doc_type,
        }
    class Meta:
        unique_together = ('application','sop')
