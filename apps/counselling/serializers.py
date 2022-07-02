from rest_framework import serializers

from apps.consultancy.serializers import ListConsultancySerializer
from apps.counselling import models
from apps.counselling.models import TestJson
from apps.institute.models import Institute, InstituteStaff
from apps.students.models import StudentModel
import uuid

class CreateInstituteCounsellingSerializer(serializers.ModelSerializer):
    interested_courses = serializers.ListSerializer(child=serializers.UUIDField(),required=False)
    class Meta:
        model =  models.InstituteCounselling
        fields = (
            'institute',
            'education_level',
            'which_time',
            'physical_counselling',
            'interested_courses',
        )



class GetInstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = (
            'id',
            'name',
            'logo',
            'country',
            'city',
            'state',
            'institute_email',
            'contact',
            'rating',

        )


class ListStudentCounsellingSerializer(serializers.ModelSerializer):
    institute = GetInstituteSerializer(read_only=True)
    interested_Course = serializers.ListSerializer(child=serializers.CharField(),source='get_interested_course')
    class Meta:
        model = models.InstituteCounselling
        fields = (
            'id',
            'institute',
            'interested_Course',
            'status',
            'which_time',
            'physical_counselling',
            'notes',
            'education_level'
        )

class GetStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentModel
        fields = '__all__'

class GetInstituteStaffSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="get_institute_full_name")
    email = serializers.CharField(source="get_institute_user_email")
    role = serializers.CharField(source="get_user_role")
    class Meta:
        model = InstituteStaff
        fields = (
            'user',
            'institute',
            'role',
            "email",
            'profile_photo',
        )


class ListInstituteCounsellingSerializer(serializers.ModelSerializer):
    student = GetStudentSerializer(read_only=True)
    interested_Course = serializers.ListSerializer(child=serializers.CharField(), source='get_interested_course')
    assign_to = GetInstituteStaffSerializer(read_only=True)
    class Meta:
        model = models.InstituteCounselling
        fields = (
            'id',
            'student',
            'interested_Course',
            'status',
            'which_time',
            'physical_counselling',
            'notes',
            'education_level',
            'assign_to',
        )

class ListInstituteStaffCounsellingSerializer(serializers.ModelSerializer):
    student = GetStudentSerializer(read_only=True)
    interested_Course = serializers.ListSerializer(child=serializers.CharField(), source='get_interested_course')

    class Meta:
        model = models.InstituteCounselling
        fields = (
            'id',
            'student',
            'interested_Course',
            'status',
            'which_time',
            'physical_counselling',
            'notes',
            'education_level',
            'assign_to',
        )

class AssignCounselorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InstituteCounselling
        fields = (
            'assign_to',
        )

class AddNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InstituteCounselling
        fields = (
            'notes',
        )

# consultancy --------------
class CreateConsultancyCounsellingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ConsultancyCounselling
        fields = (
            'consultancy',
            'education_level',
            'which_time',
            'physical_counselling',
        )


class ListStudentCounsellingOfConsultancySerializer(serializers.ModelSerializer):
    consultancy = ListConsultancySerializer(read_only=True)
    class Meta:
        model = models.ConsultancyCounselling
        fields = (
            'id',
            'consultancy',
            'status',
            'which_time',
            'physical_counselling',
            'education_level',
            'status',
            'notes',
        )

class UpdateConsultancyUser(serializers.ModelSerializer):
    class Meta:
        model = models.ConsultancyCounselling
        fields = (
            'status',
            'notes',
        )

class ConfigVarsSerializer(serializers.Serializer):
    id = serializers.UUIDField(default=uuid.uuid4)
    name = serializers.CharField(required=True)
    # user_id = serializers.IntegerField(required=True)


class ConfigFieldsSerializer(serializers.Serializer):
    data_list = serializers.ListField(child=ConfigVarsSerializer(), required=True)

class TestJsonSerializer(serializers.ModelSerializer):
    jsonData = serializers.JSONField(required=False)
    class Meta:
        model = TestJson
        fields = ('jsonData',)

    def validate_jsonData(self, value):
        serializer = ConfigFieldsSerializer(data=value)
        serializer.is_valid(raise_exception=True)
        return value
    # type
    # id
    # user_id
    # name
    # image_url
    # time stamp
    # message



