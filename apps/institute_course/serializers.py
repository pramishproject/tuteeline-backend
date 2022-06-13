
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.academic.models import Academic
from apps.institute_course import models
from rest_framework.validators import UniqueTogetherValidator

from apps.institute_course.models import CommentApplicationInstitute, Course, Faculty, InstituteApply, InstituteCourse, \
    CheckedAcademicDocument, CheckStudentIdentity, CheckedStudentLor, CheckedStudentEssay, CheckedStudentSop, \
    ApplyAction
from apps.core import fields
from apps.studentIdentity.serializers import StudentCitizenshipSerializer, StudentPassportSerializer
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
    commenter = serializers.DictField(source="commentor_name")

    class Meta:
        model = CommentApplicationInstitute
        fields = (
            'commenter',
            'created_at',
            'comment',
            'created_at',
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
    institute_name = serializers.CharField(source="get_institute_name")
    class Meta:
        model = InstituteApply
        fields = (
            'institute',
            'institute_name',
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


class GetApplyInstituteCourseDetail(serializers.ModelSerializer):
    course_name = serializers.DictField(source='get_course_data')
    faculty_name = serializers.CharField(source='get_faculty_name')
    class Meta:
        model = InstituteCourse
        fields = (
            'eligibility',
            'score',
            'last_mini_academic_score',
            'reg_fee',
            'duration_year',
            'total_fee',
            'fee_currency',
            'course_name',
            'faculty_name',
            'program',
            'intake',
            'sop',
            'lor',
            'essay',
            'passport',
            'citizenship',
            'academic',
            'reg_open',
            'reg_close',
            'reg_status',
        )

class CheckedAcademicDocumentSerializer(serializers.ModelSerializer):
    doc_name = serializers.CharField(source="get_academic_doc_name")
    class Meta:
        model = CheckedAcademicDocument
        fields = (
            'academic',
            'doc_name',
        )

class CheckedStudentEssaySerializer(serializers.ModelSerializer):
    essay_name = serializers.CharField(source='get_essay_name')
    class Meta:
        model = CheckedStudentEssay
        fields = (
            'essay',
            'essay_name'
        )

class CheckStudentIdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckStudentIdentity
        fields = (
            'citizenship',
            'passport',
        )

class CheckedStudentLorSerializer(serializers.ModelSerializer):
    lor_name = serializers.CharField(source="get_lor_name")
    class Meta:
        model =CheckedStudentLor
        fields = (
            'lor',
            'lor_name',
        )

class GetCheckedStudentSopSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='get_sop_name')
    class Meta:
        model = CheckedStudentSop
        fields = (
            'sop',
            'name',
        )
class GetMyApplicationDocumentSerializer(serializers.ModelSerializer):
    apply_to = serializers.DictField(source="institute_data")
    apply_from = serializers.DictField(source='consultancy_data')
    course = GetApplyInstituteCourseDetail(read_only=True)
    faculty= serializers.CharField(source='get_faculty_name')
    checked_student_academic= CheckedAcademicDocumentSerializer(read_only=True,many=True)
    checked_student_essay = CheckedStudentEssaySerializer(read_only=True,many=True)
    checked_student_identity = CheckStudentIdentitySerializer(read_only=True,many=False)
    checked_student_lor = CheckedStudentLorSerializer(read_only=True,many=True)
    checked_student_sop = GetCheckedStudentSopSerializer(read_only=True,many=True)
    class Meta:
        model = InstituteApply
        fields = (
            'checked_student_identity',
            'checked_student_essay',
            'checked_student_sop',
            'checked_student_academic',
            'checked_student_lor',
            'apply_to',
            'institute',
            'consultancy',
            'course',
            'faculty',
            'apply_from',
            'action',
            'view_date',
            'cancel'
        )


class CheckedAcademicDocumentInstituteSerializer(serializers.ModelSerializer):
    academic_data = serializers.DictField(source="get_academic_data")
    class Meta:
        model = CheckedAcademicDocument
        fields = (
            "academic_data",
        )

class StudentProfileDetailSerializer(serializers.ModelSerializer):
    address_relation = GetStudentAddressSerializer(many=False, read_only=True)
    class Meta:
        model = StudentModel
        fields = (
            'fullname',
            'contact',
            'image',
            'gender',
            'dob',
            'address_relation',
        )

class CheckedStudentEssayForInstituteSerializer(serializers.ModelSerializer):
    essay_data = serializers.DictField(source='get_essay_data')
    class Meta:
        model = CheckedStudentEssay
        fields = (
            'essay',
            'essay_data'
        )


class  CheckStudentIdentityForInstituteSerializer(serializers.ModelSerializer):
    citizenship = StudentCitizenshipSerializer(read_only=True,many=False)
    passport = StudentPassportSerializer(read_only=True,many=False)
    class Meta:
        model = CheckStudentIdentity
        fields = (
            'citizenship',
            'passport',
        )



class CheckedStudentLorForInstituteSerializer(serializers.ModelSerializer):
    lor_data = serializers.DictField(source="get_lor_data")
    class Meta:
        model =CheckedStudentLor
        fields = (
            'lor',
            'lor_data',
        )

class GetCheckedStudentSopForInstituteSerializer(serializers.ModelSerializer):
    sop_data = serializers.DictField(source='get_sop_data')
    class Meta:
        model = CheckedStudentSop
        fields = (
            "sop_data",
        )

class GetMyApplicationDetailForInstituteSerializer(serializers.ModelSerializer):
    apply_from = serializers.DictField(source='consultancy_data')
    apply_to = serializers.DictField(source="institute_data")
    student = StudentProfileDetailSerializer(read_only=True,many=False)
    faculty = serializers.CharField(source='get_faculty_name')
    checked_student_academic = CheckedAcademicDocumentInstituteSerializer(read_only=True, many=True)
    checked_student_essay = CheckedStudentEssayForInstituteSerializer(read_only=True, many=True)
    checked_student_identity = CheckStudentIdentityForInstituteSerializer(read_only=True, many=False)
    checked_student_lor = CheckedStudentLorForInstituteSerializer(read_only=True, many=True)
    checked_student_sop = GetCheckedStudentSopForInstituteSerializer(read_only=True, many=True)
    course_name = serializers.CharField(source="get_student_course")
    class Meta:
        model = InstituteApply
        fields = (
            'student',
            'apply_to',
            'checked_student_identity',
            'checked_student_essay',
            'checked_student_sop',
            'checked_student_academic',
            'checked_student_lor',
            'institute',
            'consultancy',
            'faculty',
            'apply_from',
            'action',
            'view_date',
            'cancel',
            'course_name',
        )


class InstituteActionSerializer(serializers.ModelSerializer):
    class Meta:
        model =ApplyAction
        fields = (
            'institute_user',
            'action',
        )
