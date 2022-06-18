import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.consultancy.models import Consultancy, ConsultancyStaff, ConsultancySocialMediaLink
from apps.core import fields
from apps.linkage.serializers import LinkageInstituteListSerializer

User = get_user_model()


class ConsultancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultancy
        fields = '__all__'


class RegisterConsultancySerializer(ConsultancySerializer):
    email = serializers.EmailField(write_only=True)
    password = fields.PasswordField()

    class Meta(ConsultancySerializer.Meta):
        fields = (
            'name',
            'email',
            'password',
            'contact',
            'country',
            'city',
            'state',
            'street_address',
            'consultancy_email',
            'latitude',
            'longitude',
            'website',
            'logo',
            'cover_image',
            'about',
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

class ConsultancySocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultancySocialMediaLink
        fields = (
            'name',
            'link',
        )

class ConsultancyDetailSerializer(serializers.ModelSerializer):
    consultancy_social_media = ConsultancySocialMediaSerializer(many=True,read_only=True)
    linkage_consultancy = LinkageInstituteListSerializer(many=True,read_only=True)
    class Meta:
        model = Consultancy
        fields = (
            "id",
            'name',
            'contact',
            'country',
            'city',
            'state',
            'street_address',
            'consultancy_email',
            'latitude',
            'longitude',
            'website',
            'logo',
            'cover_image',
            'about',
            "rating",
            "consultancy_social_media",
            "linkage_consultancy"
        )
class ConsultancyStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultancyStaff
        fields = '__all__'


class CreateConsultancyStaffSerializer(ConsultancyStaffSerializer):
    email = serializers.EmailField()
    fullname = serializers.CharField()
    profile_photo = serializers.ImageField(write_only=True)

    class Meta(ConsultancyStaffSerializer.Meta):
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


class ListConsultancyStaffSerializer(ConsultancyStaffSerializer):
    consultancy = serializers.CharField()
    email = serializers.CharField(source='get_consultancy_user_email')
    fullname = serializers.CharField(source='get_consultancy_full_name')
    role = serializers.CharField()
    is_enabled = serializers.BooleanField(source='user.is_active')
    last_logged_in = serializers.DateTimeField(source='user.last_login', format=settings.DATE_AND_TIME_FORMAT)
    created_at = serializers.DateTimeField(source='user.last_login', format=settings.DATE_AND_TIME_FORMAT)

    class Meta(ConsultancyStaffSerializer.Meta):
        fields = (
            'id',
            'consultancy',
            'email',
            'fullname',
            'role',
            'profile_photo',
            'is_enabled',
            'last_logged_in',
            'created_at'
        )


class UpdateConsultancyStaffSerializer(CreateConsultancyStaffSerializer):
    pass


class ListConsultancySerializer(ConsultancySerializer):
    class Meta(ConsultancySerializer.Meta):
        fields = (
            'id',
            'name',
            'contact',
            'country',
            'city',
            'state',
            'street_address',
            'latitude',
            'longitude',
            'website',
            'logo',
            'cover_image',
            'about',
            'rating',
            'consultancy_email',
        )


class UpdateConsultancyStaffDetail(ConsultancyStaffSerializer):
    fullname = serializers.CharField()

    class Meta(ConsultancyStaffSerializer.Meta):
        fields = (
            'fullname',
            'profile_photo',
        )


class UpdateConsultancyStaffProfilePhotoDetail(ConsultancyStaffSerializer):
    class Meta(ConsultancyStaffSerializer.Meta):
        fields = (
            'profile_photo',
        )


class DeactivateConsultancyUserSeralizer(serializers.Serializer):
    is_active = serializers.BooleanField()


class ActivateConsultancyUserSeralizer(DeactivateConsultancyUserSeralizer):
    pass
