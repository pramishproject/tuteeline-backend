import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from apps.institute.serializers import ListInstituteSerializer
from apps.students.models import CompleteProfileTracker, FavouriteInstitute, InstituteViewers, StudentAddress, StudentModel
from apps.core import fields
User = get_user_model()


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentModel
        fields = '__all__'


class RegisterStudentSerializer(StudentSerializer):
    email = serializers.EmailField(write_only=True)
    password = fields.PasswordField()

    class Meta(StudentSerializer.Meta):
        fields = (
            'fullname',
            'email',
            'password',
            'contact',
            'latitude',
            'longitude',
            'image',
            'gender',
            'dob',
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

class UpdateStudentSerializer(StudentSerializer):
    class Meta(StudentSerializer.Meta):
        fields = (
            'contact',
            'latitude',
            'longitude',
            'fullname',
            'dob',
            'gender',
            'blood_group',
        )
class UpdateProfilePictureSerializer(StudentSerializer):
    class Meta(StudentSerializer.Meta):
        fields = (
            'image',
        )

class CompleteProfileTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompleteProfileTracker
        fields = (
            'complete_address',
            'complete_academic_detail',
            'complete_parents_detail',
            'complete_citizenship_detail',
            'complete_passport_field',
            'complete_sop_field',
            'complete_personalessay_field',
            'complete_lor_field'
        )


class StudentAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAddress
        fields = (
            'state_provision',
            'country',
            'city',
            'street',
            'postal_code',
            'type',
        )

class StudentDetailSerializer(StudentSerializer):
    # user = serializers.CharField()
    address_relation = StudentAddressSerializer(many=False,read_only=True)
    email = serializers.CharField(source="get_email")
    application_tracker= CompleteProfileTrackerSerializer( read_only=True)

    class Meta(StudentSerializer.Meta):
        fields = (
            'id',
            'fullname',
            'contact',
            'latitude',
            'longitude',
            'image',
            'email',
            'blood_group',
            'application_tracker',
            'address_relation',
        )

class StudentLatitudeLongitudeUpdate(StudentSerializer):
    class Meta(StudentSerializer.Meta):
        fields = (
            'latitude',
            'longitude',
        )


        
class AddFavouriteInstituteSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavouriteInstitute
        fields = (
            'institute',
        )

class GetFavouriteInstituteSerializer(serializers.ModelSerializer):
    institute = ListInstituteSerializer(many=False,read_only=True)
    class Meta:
        model = FavouriteInstitute
        fields = (
            'student',
            'institute',
            'created_at',
            'id',
        )

class CreateInstituteVisiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteViewers
        fields = (
            'institute', 
            )

class ListVisitorHistrySerializer(serializers.ModelSerializer):
    institute = ListInstituteSerializer(many=False, read_only=True)
    class Meta:
        model = InstituteViewers
        fields = (
            'student',
            'institute',
            'created_at',
            'id',
        )
    # validators = [UniqueTogetherValidator(
    #         queryset=InstituteViewers.objects.all(),
    #         fields=['institute','student'],
    #         message="Student already visit this institute"
    #     )]