from apps.institute_course.models import InstituteCourse
import re
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import  serializers
from rest_framework.exceptions import ValidationError
from apps.institute import models

from apps.institute.models import AddInstituteFacility, Institute, InstituteScholorship,InstituteStaff, SocialMediaLink\
    ,Facility
from apps.core import fields
from apps.students.models import FavouriteInstitute

User = get_user_model()

class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = '__all__'


class RegisterInstituteSerializer(InstituteSerializer):
    email = serializers.EmailField(write_only=True)
    password = fields.PasswordField()

    class Meta(InstituteSerializer.Meta):
        fields = (
            'name',
            'institute_email',
            'category',
            'university',
            'established',
            'password',
            'contact',
            'email',
            'country',
            'city',
            'state',
            'street_address',
            'latitude',
            'longitude',
            'website',
            'logo',
            'cover_image',
            'about'

        )

        default_error_messages = {
            'duplicate_email': _('Email already exists try another one.'),
            'password_requirement_failed': _(
                'Password must 8 character  with one digit,one lowercase,one uppercase and special character.')
        }

        def validate_email(self, value):
            email = value.lower()
            if User.objects.filter(email__iexact=email).exists():
                raise serializers.ValidationError(
                    self.fail('duplicate_email')
                )
            return value

        def validate_password(self, value):
            """
            Rule 1. Password must be 8 length at minimum
            Rule 2. Password must contain one digit,one lowercase,one uppercase and special character.
            """
            pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
            matched = re.match(pattern, value)
            if not matched:
                raise serializers.ValidationError(
                    self.fail('password_requirement_failed')
                )
            return value


class InstituteStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteStaff
        fields = '__all__'

class UpdateInstituteStaffSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField()
    class Meta:
        model = InstituteStaff
        fields = (
            'fullname',
            'contact',
            'address',
        )

class UpdateInstituteStaffRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteStaff
        fields = (
            'role',
        )


class CreateInstituteStaffSerializer(InstituteStaffSerializer):
    email = serializers.EmailField()
    fullname = serializers.CharField()
    profile_photo = serializers.ImageField(write_only=True)

    class Meta(InstituteStaffSerializer.Meta):
        fields = (
            'email',
            'fullname',
            'role',
            'profile_photo',
        )

    default_error_messages = {
        'duplicate_email': _('Email already exists try another one.'),
        # 'password_requirement_failed': _(
        #     'Password must 8 character  with one digit,one lowercase,one uppercase and special character.')
    }

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                self.fail('duplicate_email')
            )
        return value


class UpdateInstituteSerializer(InstituteSerializer):
    class Meta(InstituteSerializer.Meta):
        fields = (
            'name',
            'institute_email',
            'category',
            'university',
            'established',
            'contact',
            'country',
            'city',
            'state',
            'street_address',
            'latitude',
            'longitude',
            'website',
        )
        
        def validate_email(self, value):
            email = value.lower()
            if Institute.objects.filter(email__iexact=email).exists():
                raise serializers.ValidationError(
                    self.fail('duplicate_email')
                )
            return value

class VerifyInstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = (
            'verification_status',
        )
class UpdateInstituteLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model =Institute
        fields = (
            'logo',
        )


class UpdateInstituteCoverImageSerializer(serializers.ModelSerializer):
    class Meta:
        model =Institute
        fields = (
            'cover_image',
        )
class ListInstituteSerializer(InstituteSerializer):

    class Meta(InstituteSerializer.Meta):
        fields = (
            'id',
            'name',
            'category',
            'university',
            'established',
            'contact',
            'institute_email',
            'country',
            'rating',
            'logo',
            'cover_image',
            'latitude',
            'longitude',
        )




class InstituteDetailCourseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='get_course_name')
    class Meta:
        model = InstituteCourse
        fields = (
            'name',
            'id'
        )

class FacilitySerializer(serializers.ModelSerializer):
 
    name = serializers.CharField(source='get_facility_name') 
    icon = serializers.CharField(source='get_facility_icone') 
    class Meta:
        model = AddInstituteFacility
        fields = (
            'name',
            'icon',
            'id'
        )
        
class InstituteDetailSerilaizer(serializers.ModelSerializer):
    course_related = InstituteDetailCourseSerializer(many=True,read_only =True)
    facility_related = FacilitySerializer(many=True,read_only =True)
    social_media_data = serializers.ListSerializer(child=serializers.DictField(),source="social_media")

    is_favourite = serializers.SerializerMethodField()

    def get_is_favourite(self, obj):
        institute_id = obj.id
        student_id = self.context['request'].GET.get('student_id', None)
        if student_id != None:
            try:
                fav = FavouriteInstitute.objects.get(institute=institute_id,student=student_id)
                return str(fav.id)
            except FavouriteInstitute.DoesNotExist:
                return ""
        return ""

    class Meta:
        model = Institute
        fields = (
            'name',
            'category',
            'university',
            'established',
            'contact',
            'institute_email',
            'country',
            'logo',
            'cover_image',
            'about',
            'website',
            'longitude',
            'latitude',
            'state',
            'city',
            'street_address',
            'facility_related',
            'course_related',
            'social_media_data',
            'is_favourite',
            'brochure',
        )


class AddScholorshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteScholorship
        fields = (
            'topic',
            'description'
        )

class GetScholorshipSerializer(AddScholorshipSerializer):
    class Meta(AddScholorshipSerializer.Meta):
        fields = (
            'id',
            'topic',
            'description'
        )


class InstituteStaffSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="get_institute_user_email")
    user_name= serializers.CharField(source="get_institute_full_name")
    user_role = serializers.CharField(source="get_user_role")
    class Meta:
        model = InstituteStaff
        fields = (
            'id',
            'created_at',
            'updated_at',
            'email',
            'user_name',
            'user_role',
            'profile_photo',
        )


class CreateInstituteStaffSerializer(InstituteStaffSerializer):
    email = serializers.EmailField()
    fullname = serializers.CharField()
    profile_photo = serializers.ImageField(write_only=True)

    class Meta(InstituteStaffSerializer.Meta):
        model = InstituteStaff
        fields = (
            'email',
            'fullname',
            'role',
            'profile_photo',
        )

class AddSocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaLink
        fields = (
            'name',
            'link'
        )

class GetSocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaLink
        fields = (
            'id',
            'name',
            'link'
        )


class AddInstituteFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = AddInstituteFacility
        fields = (
            'facility',
        )

class FacilityListSerializer(serializers.ModelSerializer):
    class Meta:
        model =Facility
        fields = (
            'id',
            'name',
            'icon',
        )

class UpdateBrochureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = (
            'brochure',
        )