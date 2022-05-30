from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.college import models
from apps.college.models import College, Faculty, Course, CourceDetail, Gallery, RestrictCountry, CounselorModel, \
    Accomodation, Canteen, Laboratory, LibraryModel, Blog, Facility
from apps.student.models import StudentApply, Comment
from apps.student.utils.file_function import pdfformat

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['email', 'password']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'is_active', 'is_admin', 'is_institute', 'is_student']


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.College
        fields = ['id', 'name', 'contact', 'website', 'email', 'category', 'university', 'brochure', 'established',
                  'logourl', 'coverpage', 'country', 'lat', 'long', 'type', 'schlorship', 'review', 'location', 'about']


class CollegeCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.College
        fields = ['id', 'name', 'category', 'university', 'established', 'logourl', 'coverpage', 'country', 'review']


class CollegeDataUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.College
        fields = ['name', 'contact', 'email', 'category', 'university', 'established', 'website', 'approved_by']


class AboutUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.College
        fields = ['about']


class CollegeLogoUpdate(serializers.ModelSerializer):
    class Meta:
        model = models.College
        fields = ['logourl']


class CollegeCoverpageUpdate(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['coverpage']


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'name', 'description']


class FetchCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CourceDetailInsertSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourceDetail
        fields = '__all__'


class CourseDetailEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourceDetail
        fields = ['description', 'eligibility_exam', 'score', 'min_gpa', 'Duration', 'Intake', 'fee', 'feeCurrency',
                  'photo', 'citizenship', 'passport', 'school_certificate', 'highschool_certificate',
                  'undergraduate_certificate', 'graduate_certificate']


# class ScholorshipScheamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=ScholorshipSchems
#         fields='__all__'

# class MinimumDocSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=MinimumDoc
#         fields='__all__'

class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['facility']


# class StudentMinimumDocumentDescriptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=StudentMinimumDocumentDescription
#         fields=['minimum_doc_id','course_criteria_id','description']

class GallerySerializer(serializers.ModelSerializer):
    # college=CollegeSerializer()
    class Meta:
        model = Gallery
        fields = '__all__'


class CollegeGallertStudentpage(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ['status', 'picture', 'date']


# class CourseDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CourceDetail
#         fields='__all__'


class CheckCollegeAccountCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password1 = serializers.CharField(max_length=200)
    password2 = serializers.CharField(max_length=200)
    name = serializers.CharField(max_length=200)
    contact = serializers.CharField(max_length=200)
    category = serializers.CharField(max_length=200)
    university = serializers.CharField(max_length=200)
    established = serializers.CharField(max_length=200)
    logourl = serializers.FileField()
    coverpage = serializers.FileField()
    lat = serializers.FloatField()
    long = serializers.FloatField()
    brochure = serializers.FileField(validators=[pdfformat], default=None)


class StudentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentApply
        fields = ['id', 'student', 'course', 'first_name', 'middle_name', 'last_name', 'status', 'apply_date', 'view',
                  'student_action', 'enrolled']


class RestrictCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = RestrictCountry
        fields = '__all__'


class GetCountryRestrictedSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestrictCountry
        fields = ['id', 'country']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['lat', 'long', 'location']


class CourceDetailFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourceDetail
        fields = ['form_fee', 'form', 'openDate', 'closeDate']


class CouncilorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounselorModel
        fields = '__all__'


class AccomodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accomodation
        fields = '__all__'


class CanteenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canteen
        fields = '__all__'


class LaboratorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratory
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryModel
        fields = "__all__"


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"
