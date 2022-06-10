
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.academic.models import Academic
from apps.institute_course import models
from rest_framework.validators import UniqueTogetherValidator

from apps.institute_course.models import CommentApplicationInstitute, Course, Faculty, InstituteApply, InstituteCourse
from apps.core import fields
from apps.students.models import StudentModel,StudentAddress
from apps.institute.models import Institute


User = get_user_model()

class InstituteCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteCourse
        fields = '__all__'
        # validators = [UniqueTogetherValidator(
        #     queryset=InstituteCourse.objects.all(),
        #     fields=['institute','course']
        # )]

class AddInstituteCourseSerializer(InstituteCourseSerializer):
    class Meta(InstituteCourseSerializer.Meta):
        fields = (
            'program',
            'faculty',
            'course',
            'intake',
            'eligibility',
            'score',
            'last_mini_academic_score',
            'duration_year',
            'total_fee',
            'fee_currency',
            'reg_status',
            'reg_open',
            'reg_close', 
            'academic',
            'citizenship',  
            'passport', 
            'essay', 
            'lor', 
            'sop'
        )
        # validators = [UniqueTogetherValidator(
        #     queryset=InstituteCourse.objects.all(),
        #     fields=['institute','course'],
        #     message="This Course Already Exist"
        # )]
    # def validate(self, attrs):
    #     attrs = super().validate(attrs)

    #     if "institute" in attrs and "course" in attrs:
    #         try:
    #             self.institute = InstituteCourse.objects.get(institute=attrs['institute'],course=attrs['course'])
            
    #         except InstituteCourse.DoesNotExist:

    #             pass

    #         del attrs['id']
    #     return attrs

    # def create(self, validate_data):
    #     return InstituteCourse.objects.get_or_create(**validate_data)

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            'id',
            'name',
            'description'
        )

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = (
            'name',
            'id'
        )


class ListInstituteCourseSerializer(InstituteCourseSerializer):

    course = CourseSerializer(read_only =True)
    faculty =FacultySerializer(read_only = True)
    # related_student_is_apply = serializers.SerializerMethodField()

    # @classmethod
    # def get_related_student_is_apply(self,obj ): #TODO implement
    #     pass

    class Meta(InstituteCourseSerializer.Meta):
            fields = (
                'id',
                'program',
                'faculty',
                'course',
                'intake',
                'eligibility',
                'score',
                'last_mini_academic_score',
                'duration_year',
                'total_fee',
                'fee_currency',
                'reg_status',
                'reg_open',
                'reg_close',
                'academic',
                'citizenship',
                'passport',
                'essay',
                'lor',
                'sop',

            )

    
class CommentApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentApplicationInstitute
        fields = (
            'institute_user',
            'comment'
        )

class ListApplicationCommentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="commentor_name")

    class Meta:
        model = CommentApplicationInstitute
        fields = (
            'name',
            'created_at',
            'comment'
        )
class StudentApplySerializer(serializers.ModelSerializer):
    academic = serializers.ListSerializer(child=serializers.UUIDField(),write_only=True,
                                          required=False,allow_empty=True)
    citizenship = serializers.CharField(write_only=True,required=False, allow_blank=True)
    passport = serializers.CharField(write_only=True,required=False,allow_blank=True)
    lor = serializers.ListSerializer(child=serializers.UUIDField(),write_only=True,required=False,allow_empty=True)
    sop = serializers.CharField(write_only=True,required=False,allow_blank=True)
    essay = serializers.CharField(write_only=True,required=False,allow_blank=True)
    class Meta:
        model = InstituteApply
        fields = (
            'student',
            'course',
            'institute',
            'consultancy',
            'academic',
            'citizenship',
            'passport',
            'lor',
            'sop',
            'essay'
        )


class StudentMyApplicationListSerializer(serializers.ModelSerializer):
    apply_to = serializers.DictField(source="institute_data")
    consultancy_name = serializers.CharField(source='get_consultancy_name')
    course = serializers.CharField(source='get_student_course')

    class Meta:
        model = InstituteApply
        fields = (
            'id',
            'apply_to',
            'consultancy_name',
            'consultancy',
            'institute',
            'course',
            'created_at',
            'updated_at',
            'action',
            'action_data',
            'view_date',
            'forward',
            'cancel',
        )
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=InstituteApply.objects.all(),
        #         fields=['student', 'course'],
        #         message="One student can apply one course"
        #     )
        # ]


class GetStudentAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAddress
        fields = ['state_provision','country']

class GetStudentApplicantSerializer(serializers.ModelSerializer):
    address_relation=GetStudentAddressSerializer(many=False,read_only =True)
    class Meta:
        model = StudentModel
        fields = (
            'fullname',
            'address_relation'
            )

class ApplicationInstituteCourseSerializer(InstituteCourseSerializer):

    course = CourseSerializer(read_only =True)
    class Meta(InstituteCourseSerializer.Meta):
        fields = (
            'course',
        )

# class GetStudentApplicationInstituteSerializer(serializers.ModelSerializer):
#     student = GetStudentApplicantSerializer(many=False,read_only =True)
#     course = ApplicationInstituteCourseSerializer(many=False,read_only =True)
#     # consultancy = serializers.CharField()

#     class Meta:
#         model = InstituteApply
#         fields = (
#             'student',
#             'course',
#             'consultancy',
#             'action',
#             'cancel',
#             'created_at'
#         )

class CancelStudentApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteApply
        fields = (
            'cancel',
        )


class GetStudentApplicationInstituteSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='get_student_user_name')
    consultancy_name = serializers.CharField(source='get_consultancy_name')
    course_name = serializers.CharField(source='get_student_course') 
    address = serializers.CharField(source='student_address')
    class Meta:
        model = InstituteApply
        fields = (
            'institute',
            'id',
            'student',
            'student_name',
            'course_name',
            'course',
            'consultancy_name',
            'consultancy',
            'action',
            'cancel',
            'created_at',
            'address',
        )

class GetStudentApplicationStudentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='get_student_user_name')
    consultancy_name = serializers.CharField(source='get_consultancy_name')

    course = serializers.CharField(source='get_student_course') 
    address = serializers.CharField(source='student_address')
    class Meta:
        model = InstituteApply
        fields = (
            'id',
            'student',
            'student_name',
            'course',
            'consultancy',
            'consultancy_name',
            'institute',
            'institute_name',
            'action',
            'cancel',
            'created_at',
            'address',
        )

class ApplicationSerializerDashboard(serializers.Serializer):
    action = serializers.CharField()
    action__count = serializers.IntegerField()

# <BaseModelQuerySet [{'action': 'applied', 'action__count': 1}, {'action': 'verify', 'action__count': 1}]>

class StudentAdmissionApplicationSerializer(serializers.ModelSerializer):
    """
    application detail , course detail,application status,comment,sended document
    """
    class Meta:
        model = InstituteApply
        fields = (
            'student',
            'course',
            "consultancy",
            'action',
            'action_data',
            'institute',
            'action_institute_user',
            'action_consultancy_user',
            'view_date',
            'forward',
            'cancel',
        )


class GetInstituteCompareDetail(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = (
            'id',
            'name',
            'university',
            'established',
            'rating',
            'country',
            'city',
            'state',
            'street_address',
            'type',
            'logo',
        )
class CompareInstituteSerializer(serializers.ModelSerializer):
    institute = GetInstituteCompareDetail(read_only=True)
    course_name = serializers.CharField(source="get_course_name")
    faculty_name = serializers.CharField(source="get_faculty_name")
    class Meta:
        model = InstituteCourse
        fields = (
            'course_name',
            'institute',
            'faculty_name',
            'program',
            'intake',
            'eligibility',
            'score',
            'last_mini_academic_score',
            'duration_year',
            'total_fee',
            'reg_fee',
            'fee_currency',
            'academic',
            'lor',
            'sop',
            'citizenship',
            'passport',
            'essay'
        )

class StudentAccessDetail(serializers.Serializer):
    academics = serializers.ListSerializer(child=serializers.CharField())