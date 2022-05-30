from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import LORModel, Bookmark, Student, AcademicInfo, Eligibility, PassportModel, StudentApply, Parents, \
    VisitedCollege, StudentEssay, CitizenshipModel
from ..college.serializers import CollegeCardSerializer

User = get_user_model()


class UserCreateCustomSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=200)
    middle_name = serializers.CharField(max_length=200, allow_blank=True)
    last_name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    password1 = serializers.CharField(max_length=200)
    password2 = serializers.CharField(max_length=200)
    contact = serializers.CharField(max_length=200)
    dob = serializers.DateField()
    gender = serializers.CharField(max_length=30, default="Male")
    country = serializers.CharField(max_length=100)
    street_name = serializers.CharField(max_length=100, allow_blank=True)
    city_town = serializers.CharField(max_length=200, allow_blank=True)
    state_provision = serializers.CharField(max_length=200)
    postal_code = serializers.IntegerField()


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class StudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['contact', 'dob', 'gender', 'country', 'street_name', 'city_town', 'state_provision', 'postal_code']


class StudentApplicationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['contact', 'dob', 'gender', 'country', 'street_name', 'city_town', 'state_provision', 'postal_code',
                  'photo']


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['email', 'password']


class StudentProfileUpdate(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['photo']


class AcademicSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicInfo
        fields = "__all__"


class StudentAllDetailSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = AcademicInfo
        fields = "__all__"


class AcademicUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicInfo
        fields = ['Institute_name', 'level', 'percentage', 'duration']


class AcademicCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicInfo
        fields = ['certificate']


class AcademicMarksheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicInfo
        fields = ['marksheet']


class EligibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Eligibility
        fields = '__all__'


class EligibilityCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eligibility
        fields = ['certificate']


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name']


class StudentApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentApply
        fields = '__all__'


class UpdateStatusSeializer(serializers.ModelSerializer):
    class Meta:
        model = StudentApply
        fields = ['enrolled', 'status', 'action_date']


class ParentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parents
        fields = '__all__'


class VisitedCollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitedCollege
        fields = '__all__'


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = "__all__"


class BookmarkGetCollegeSerializer(serializers.ModelSerializer):
    college = CollegeCardSerializer()

    class Meta:
        model = Bookmark
        fields = "__all__"


class GetApplyDataSerializer(serializers.ModelSerializer):
    college = CollegeCardSerializer()

    class Meta:
        model = StudentApply
        fields = "__all__"


class UpdateStudentAction(serializers.ModelSerializer):
    class Meta:
        model = StudentApply
        fields = ['student_action']


class VisitedCollegeSerializer(serializers.ModelSerializer):
    college = CollegeCardSerializer()

    class Meta:
        model = VisitedCollege
        fields = "__all__"


class CollegeVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitedCollege
        fields = "__all__"


# class SOPSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=StudentSOP
#         fields="__all__"

class StudentEssaySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEssay
        fields = "__all__"


class StudentEssayUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEssay
        fields = ['topic', 'essay']


class CitizenshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitizenshipModel
        fields = "__all__"


class PassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassportModel
        fields = "__all__"


class LorSerializer(serializers.ModelSerializer):
    class Meta:
        model = LORModel
        fields = "__all__"
