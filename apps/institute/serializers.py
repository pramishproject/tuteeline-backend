from apps.institute_course.models import InstituteCourse
import re
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, serializers
from rest_framework.exceptions import ValidationError
from apps.institute import models

from apps.institute.models import AddInstituteFacility, Institute, InstituteScholorship,InstituteStaff, SocialMediaLink
from apps.core import fields

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
            'social_media_data'
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
    class Meta:
        model = InstituteStaff
        fields = '__all__'


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