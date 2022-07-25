from apps.students.exceptions import StudentModelNotFound
from apps.students.models import StudentModel
import re
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.datetime_safe import datetime
from django.utils.timezone import now
from django.utils.translation import ugettext as _


from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.serializers import (
    TokenObtainSerializer,
    TokenRefreshSerializer,
    PasswordField
)
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from apps.auth.jwt.cache import LoginCache
from apps.consultancy.exceptions import ConsultancyUserEmailNotFound, PortalUserEmailNotFound
from apps.institute.exceptions import InstituteUserEmailNotFound
from apps.consultancy.models import ConsultancyStaff
from apps.institute.models import InstituteStaff
from apps.core import fields
from apps.portal.models import PortalStaff
from apps.pyotp.mixins import OTPMixin
from apps.settings.exceptions import SettingsNotFound
from apps.settings.models import Settings
from apps.user.models import ConsultancyUser, InstituteUser, PortalUser

User = get_user_model()


class CustomTokenObtainSerializer(TokenObtainSerializer):

    @classmethod
    def get_token(cls, user):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'] = PasswordField()

    def validate(self, attrs):
        cache_results = LoginCache.get(attrs['username'])
        lockout_timestamp = None
        invalid_attempt_timestamps = cache_results['invalid_attempt_timestamps'] if cache_results else []

        invalid_attempt_timestamps = [timestamp for timestamp in invalid_attempt_timestamps if
                                      timestamp > (datetime.now() - timedelta(minutes=15))]

        if len(invalid_attempt_timestamps) >= 5:
            raise serializers.ValidationError(
                _('too many attempts, account locked ! wait for 15 minutes'),
            )

        self.user = self.authenticate(username=attrs['username'], password=attrs['password'])
        if self.user is None:
            invalid_attempt_timestamps.append(datetime.now())
            if len(invalid_attempt_timestamps) >= 5:
                lockout_timestamp = datetime.now()
                raise serializers.ValidationError(
                    _('locked.')
                )
            LoginCache.set(attrs['username'], invalid_attempt_timestamps, lockout_timestamp)
            raise serializers.ValidationError(
                _('Email or Password does not matched .'),
            )
        if self.user:
            if not self.user.is_active:
                msg = _('User account is not activated.')
                raise PermissionDenied(msg)

            if self.user.is_archived:
                msg = _('User is archived.')
                raise PermissionDenied(msg)
        LoginCache.delete(attrs['username'])
        return {}

    @staticmethod
    def authenticate(username, password):
        try:
            user = User.objects.get(
                Q(email=username) | Q(username=username)
            )
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            User().set_password(password)


class LoginSerializer(CustomTokenObtainSerializer):

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            self.validate_user()
            student=StudentModel.objects.get(user=self.user.id)
            refresh = self.get_token(self.user)

            data['refresh_token'] = str(refresh)
            data['token'] = str(refresh.access_token)
            data['sid']=str(student.pk)
            data['id']=str(self.user.id)
            self.user.last_login = now()
            self.user.save()
            return data
        except StudentModel.DoesNotExist:
            raise StudentModelNotFound
        

    def validate_user(self):
        pass


class StudentUserLoginSerializer(LoginSerializer):
    def validate(self, attrs):
        data = super(StudentUserLoginSerializer, self).validate(attrs)
        # user detail
        data['user'] = self.user
        return data


class StudentUserLoginResponseSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)
    sid = serializers.CharField()
    id = serializers.CharField()

# class ConsultancyUserLoginSerializer(LoginSerializer):
#     def validate_user(self):
#         if self.user.user_type != 'consultancy_user':
#             raise serializers.ValidationError(
#                 _('Email or Password does not matched.'),
#             )

class InstituteUserLoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=PasswordField()

    def validate_email(self, value):
        try:
            InstituteUser.objects.get(email=value)
        except InstituteUser.DoesNotExist:
            raise InstituteUserEmailNotFound

        return value

class ConsultancyUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = PasswordField()

    def validate_email(self, value):
        try:
            ConsultancyUser.objects.get(email=value)
        except ConsultancyUser.DoesNotExist:
            raise ConsultancyUserEmailNotFound
        return value


class PortalUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = PasswordField()

    def validate_email(self, value):
        try:
            PortalUser.objects.get(email=value)
        except PortalUser.DoesNotExist:
            raise PortalUserEmailNotFound
        return value


class ResendOTPCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    default_error_messages = {
        'invalid_email': _('Invalid email.')
    }

    def validate_email(self, value):
        try:
            self.user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(self.fail('invalid_email'))
        return value


class CodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)


class VerifyConsultanyUserOTPSerializer(CodeSerializer, OTPMixin):
    """
    Use this to activate any user
    """

    def get_token(self, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        attrs = super(VerifyConsultanyUserOTPSerializer, self).validate(attrs)
        # get current user from views
        user = self.context['view'].get_object()
        # check for otp code validation

        consultancy_staff = ConsultancyStaff.objects.get(user=user)
        position=consultancy_staff.role.name
        try:
            color = Settings.objects.get(user=user).color
        except Settings.DoesNotExist:
            raise SettingsNotFound
        is_code_valid = self.verify_otp_for_user(user, attrs['code'], '2FA')
        if is_code_valid:
            data = super().validate(attrs)
            refresh = self.get_token(user)
            data['refresh_token'] = str(refresh)
            data['token'] = str(refresh.access_token)
            data['role'] = position
            data['color'] = color
            data['id']=consultancy_staff.consultancy.id
            user.last_login = now()
            user.save()
            return data
        else:
            raise serializers.ValidationError(
                {'code': _('Invalid code.')}
            )


class VerifyPortalUserOTPSerializer(CodeSerializer,OTPMixin):
    """
    Use this to activate portal user
    """

    def get_token(self, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        attrs = super(VerifyPortalUserOTPSerializer, self).validate(attrs)
        # get current user from views
        user = self.context['view'].get_object()
        # check for otp code validation
        position = PortalStaff.objects.get(user=user).role.name
        try:
            color = Settings.objects.get(user=user).color
        except Settings.DoesNotExist:
            raise SettingsNotFound
        is_code_valid = self.verify_otp_for_user(user, attrs['code'], '2FA')
        if is_code_valid:
            data = super().validate(attrs)
            refresh = self.get_token(user)
            data['refresh_token'] = str(refresh)
            data['token'] = str(refresh.access_token)
            data['role'] = position
            data['color'] = color
            data['id']=user.id
            user.last_login = now()
            user.save()
            return data
        else:
            raise serializers.ValidationError(
                {'code': _('Invalid code.')}
            )

class VerifyInstituteUserOTPSerializer(CodeSerializer,OTPMixin):
    """
    Use this to activate portal user
    """

    def get_token(self, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        attrs = super(VerifyInstituteUserOTPSerializer, self).validate(attrs)
        # get current user from views
        user = self.context['view'].get_object()
        # check for otp code validation
        position = InstituteStaff.objects.get(user=user)
        try:
            color = Settings.objects.get(user=user).color
        except Settings.DoesNotExist:
            raise SettingsNotFound
        is_code_valid = self.verify_otp_for_user(user, attrs['code'], '2FA')
        if is_code_valid:
            data = super().validate(attrs)
            refresh = self.get_token(user)
            data['refresh_token'] = str(refresh)
            data['token'] = str(refresh.access_token)
            data['role'] = position.role.name
            data['color'] = color
            data['id']=user.id
            data["staff_id"] = str(position.id)
            data["institute_id"] = str(position.institute.pk)
            user.last_login = now()
            user.save()
            return data
        else:
            raise serializers.ValidationError(
                {'code': _('Invalid code.')}
            )


class CustomTokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])

        data = {'token': str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data['refresh_token'] = str(refresh)

        return data


class UserIdResponseSerializer(serializers.Serializer):
    id = serializers.CharField()

class UserLoginSerializer(serializers.Serializer):
    id = serializers.CharField()

class NormalUserLoginDetailSerializer(serializers.Serializer):
    fullname = serializers.CharField()
    avatar = serializers.ImageField(source='normaluser.avatar')


class NormalUserLoginResponseSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)
    role = serializers.CharField()
    color = serializers.CharField()
    id = serializers.CharField()
    institute_id = serializers.CharField(required=False)
    staff_id = serializers.CharField(required=False)
    user_detail = NormalUserLoginDetailSerializer(source='user', read_only=True)


class ConsultancyUserLoginResponseSerializer(NormalUserLoginResponseSerializer):
    user_detail = None


class CreatePasswordForConsultancyStaffSerializer(serializers.Serializer):
    password = fields.PasswordField()

    default_error_messages = {
        'password_requirement_failed': _(
            'Password must 8 character  with one digit,one lowercase,one uppercase and special character.')
    }

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


class CreatePasswordForPortalStaffSerializer(CreatePasswordForConsultancyStaffSerializer):
    pass


class ConsultancyUserChangePasswordSerializer(serializers.Serializer):
    old_password = PasswordField()
    new_password = PasswordField()
    confirm_new_password = PasswordField()

    default_error_messages = {
        'password_requirement_failed': _(
            'Password must 8 character  with one digit,one lowercase,one uppercase and special character.'),
        'password_same': _("Old password is same as new password"),
        'password_not_in_db': _("Your existing old password does n\'t match with our database please try "
                                "again"),
        'password_not_matched': _("Password not matched please conform your password again."),

    }

    def validate_password(self, value):
        user = self.context['view'].get_object()
        if not (user.check_password(value)):
            raise serializers.ValidationError(self.fail('password_not_in_db'))
        return value

    def validate(self, attrs):
        """
        Rule 1. Password must be 8 length at minimum
        Rule 2. Password must contain one digit,one lowercase,one uppercase and special character.
        Rule 3. New password must not match old password
        Rule 4. New password and confirm password fields must be same.
        """
        pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        matched = re.match(pattern, attrs['new_password'])
        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError(self.fail('password_same'))
        if matched:
            if attrs['new_password'] != attrs['confirm_new_password']:
                raise serializers.ValidationError(self.fail('password_not_matched'))
        else:
            raise serializers.ValidationError(
                self.fail('password_requirement_failed')
            )
        return attrs

class GetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ChangeForgetPasswordSerializer(serializers.Serializer):
    new_password = PasswordField()
    confirm_new_password = PasswordField()

    default_error_messages = {
        'password_requirement_failed': _(
            'Password must 8 character  with one digit,one lowercase,one uppercase and special character.'),
        'password_same': _("Old password is same as new password"),
        'password_not_in_db': _("Your existing old password does n\'t match with our database please try "
                                "again"),
        'password_not_matched': _("Password not matched please conform your password again."),

    }

    def validate_password(self, value):
        user = self.context['view'].get_object()
        if not (user.check_password(value)):
            raise serializers.ValidationError(self.fail('password_not_in_db'))
        return value

    def validate(self, attrs):
        """
        Rule 1. Password must be 8 length at minimum
        Rule 2. Password must contain one digit,one lowercase,one uppercase and special character.
        Rule 3. New password must not match old password
        Rule 4. New password and confirm password fields must be same.
        """
        pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        matched = re.match(pattern, attrs['new_password'])
        if matched:
            if attrs['new_password'] != attrs['confirm_new_password']:
                raise serializers.ValidationError(self.fail('password_not_matched'))
        else:
            raise serializers.ValidationError(
                self.fail('password_requirement_failed')
            )
        return attrs

class VerifySerializer(serializers.Serializer):
    verify = serializers.BooleanField()