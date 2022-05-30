import re

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from apps.core import fields
from apps.portal.models import PortalStaff

User = get_user_model()


# class RegisterPortalSerializer(PortalSerializer):
#     email = serializers.EmailField(write_only=True)
#     password = fields.PasswordField()
#
#     class Meta(PortalSerializer.Meta):
#         fields = (
#             'name',
#             'email',
#             'password',
#             'address',
#             'country',
#             'city',
#             'state',
#             'profile_picture',
#             'street_address',
#             'latitude',
#             'longitude',
#         )
#
#     default_error_messages = {
#         'duplicate_email': _('Email already exists try another one.'),
#         'password_requirement_failed': _(
#             'Password must 8 character  with one digit,one lowercase,one uppercase and special character.')
#     }
#
#     def validate_email(self, value):
#         email = value.lower()
#         if User.objects.filter(email__iexact=email).exists():
#             raise serializers.ValidationError(
#                 self.fail('duplicate_email')
#             )
#         return email
#
#     def validate_password(self, value):
#         """
#         Rule 1. Password must be 8 length at minimum
#         Rule 2. Password must contain one digit,one lowercase,one uppercase and special character.
#         """
#         pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
#         matched = re.match(pattern, value)
#         if not matched:
#             raise serializers.ValidationError(
#                 self.fail('password_requirement_failed')
#             )
#         return value


class PortalStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortalStaff
        fields = '__all__'


class CreatePortalStaffSerializer(PortalStaffSerializer):
    email = serializers.EmailField()
    fullname = serializers.CharField()

    class Meta(PortalStaffSerializer.Meta):
        fields = (
            'email',
            'role',
            'fullname',
        )

    default_error_messages = {
        'duplicate_email': _('Email already exists try another one.'),
        'password_requirement_failed': _(
            'Password must minimum 8 character  with one digit,one lowercase,one uppercase and special character.')
    }

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                self.fail('duplicate_email')
            )
        return email

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
