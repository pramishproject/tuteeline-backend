import os
from datetime import timedelta

from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError, PermissionDenied

from apps.auth.jwt.emails import EmailVerificationEmail
from apps.core import usecases
from apps.core.usecases import CreateUseCase, BaseUseCase
from apps.pyotp.mixins import OTPMixin
from apps.pyotp.models import PyOTP
from apps.user.models import ConsultancyUser, PortalUser
from apps.settings.models import Settings

User = get_user_model()


class UserLoginWithOTPUseCase(CreateUseCase, OTPMixin):
    def __init__(self, request, serializer):
        self._request = request
        super().__init__(serializer)
    def execute(self):
        self._factory()
        # print(self._user.id)
        return {'id': self._user.id}

    def _factory(self):
        credentials = {
            'username': self._data['email'],
            'password': self._data['password']
        }
        self._user = authenticate(self._request, **credentials)
        if self._user is not None:
            """
            Sends email confirmation mail to the user's email
            :return: None
            """
            setting = Settings.objects.get(user=self._user)
            # test
            # code = self._generate_totp(
            #     user=self._user,
            #     purpose='2FA',
            #     interval=1800
            # )
            # print("code",code)
            if setting.two_fa:
                code = self._generate_totp(
                    user=self._user,
                    purpose='2FA',
                    interval=180
                )
                send_to = os.getenv("DEFAULT_EMAIL", self._user.email)
                EmailVerificationEmail(
                    context={
                        'code': code,
                        'uuid': self._user.id
                    }
                ).send(to=[send_to])


        else:
            raise PermissionDenied(
                {
                    'authentication_error': _('User name or password not matched')
                }
            )


# class InstituteUserLoginWithOTPUseCase(CreateUseCase, OTPMixin):
#     def __init__(self, request,serializer):
#         self._request = request
#         super().__init__(serializer)
#     def execute(self):
#         self._factory()


class ResendOTPCodeUseCase(CreateUseCase, OTPMixin):
    """
    Use this endpoint to resend otp
    """

    def __init__(self, serializer):
        self._serializer = serializer
        self._user = self._serializer.user
        super().__init__(self._serializer)

    def execute(self):
        self.is_valid()
        self._factory()

    def is_valid(self):
        # wait for 2 minutes.
        try:
            old_otp = PyOTP.objects.get(
                user=self._user,
                purpose='2FA'
            )
        except PyOTP.DoesNotExist:
            raise ValidationError({
                'non_field_errors': _('Has no old OTP')
            })

        if old_otp.created_at + timedelta(minutes=2) > timezone.now():
            raise ValidationError({
                'non_field_errors': _('OTP Resend  can be performed only after 2 minutes.')
            })

    def _factory(self):
        code = self._regenerate_totp(self._user, '2FA')
        EmailVerificationEmail(
            context={
                'code': code,
                'uuid': self._user.id
            }
        ).send(to=[self._user.email])


class ChangeConsultancyUserPasswordUseCase(BaseUseCase):
    def __init__(self, serializer, consultancy_user):
        self._serializer = serializer
        self._data = serializer.validated_data
        self._consultancy_user = consultancy_user

    def execute(self):
        self._factory()

    def _factory(self):
        password = self._data.pop('confirm_new_password')
        self._consultancy_user.set_password(password)
        self._consultancy_user.save()


class UpdatePassportUseCase(BaseUseCase):
    def __init__(self, serializer, user):
        self._serializer = serializer
        self._data = serializer.validated_data
        self._user = user

    def execute(self):
        self._factory()

    def _factory(self):
        password = self._data.pop('confirm_new_password')
        self._user.set_password(password)
        self._user.save()


class CreatePasswordForConsultancyUserUseCase(usecases.CreateUseCase):
    def __init__(self, serializer, consultancy_user: ConsultancyUser):
        self._consultancy_user = consultancy_user
        super().__init__(serializer)

    def execute(self):
        self._factory()

    def _factory(self):
        password = self._data.pop('password')
        self._consultancy_user.set_password(password)
        self._consultancy_user.save()


class CreatePasswordForPortalUserUseCase(usecases.CreateUseCase):
    def __init__(self, serializer, portal_user: PortalUser):
        self._portal_user = portal_user
        super().__init__(serializer)

    def execute(self):
        self._factory()

    def _factory(self):
        password = self._data.pop('password')
        self._portal_user.set_password(password)
        self._portal_user.save()
