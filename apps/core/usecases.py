import csv
import os
from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework_simplejwt.tokens import RefreshToken
from apps.pyotp.mixins import OTPMixin
from apps.core.email import SendConfirmationEmail
from apps.core.utils import update
from apps.core import task
User = get_user_model()


from django.urls import reverse

class BaseUserUseCase(OTPMixin):
    def _send_email(self, user, request,path):
        self.user_instance = user
        self._request = request
        token = RefreshToken.for_user(user=self.user_instance)
        # get current site
        current_site = get_current_site(self._request).domain
        # we are calling verify by email view  here whose name path is activate-by-email
        # relative_link = reverse('activate-by-email')
        # make whole url
        absolute_url = request.build_absolute_uri('/')[:-1]+"/"+str(self.user_instance.pk)+"/"+ path + "?token=" + str(token)
        # absolute_url = 'http://localhost:3000' + relative_link + "?token=" + str(token)
        self.context = {
            'user': self.user_instance.fullname,
            'url': absolute_url
        }
        receipent = self.user_instance.email
        send_to = os.getenv("DEFAULT_EMAIL", self.user_instance.email)
        SendConfirmationEmail(context=self.context).send(to=[send_to])
        # context = {
        #         'uuid': portal_user.id,
        #         'name': portal_user.fullname +"with celery",
        #         'user_email': send_to,
        #     }
        # self.context = {
        #     'user': self.user_instance.fullname,
        #     'url': absolute_url,
        #     'user_email': send_to,
        # }
        #     # print("******",context)
        # task.send_set_confirmation_email_to_user.apply_async(
        #         kwargs=self.context
        #     )
        # send_email.delay(receipent, **self.context)
        # if use_celery:
        #     print("celeryunsbd hcvbds")
        #     context = {
        #         'uuid': portal_user.id,
        #         'name': portal_user.fullname +"with celery",
        #         'user_email': send_to,
        #     }
        #     # print("******",context)
        #     tasks.send_set_password_email_to_user.apply_async(
        #         kwargs=context
        #     )
        # else:
        #     # without celery
        #     print("send email")

    def _send_verification_email(self,user,request):
        code = self._generate_totp(
            user=user,
            purpose='2FA',
            interval=60*60*2
        )
        print(user,request,code)

class BaseUseCase:
    """
    Base Use Case
    """

    def execute(self):
        raise NotImplementedError("Subclasses should implement this!")

    def _factory(self):
        raise NotImplementedError("Subclasses should implement this!")

    def is_valid(self):
        return True


class CreateUseCase(BaseUseCase):
    def __init__(self, serializer):
        self._serializer = serializer
        self._data = self._serializer.validated_data

    def execute(self):
        self.is_valid()
        self._factory()


class UpdateUseCase(BaseUseCase):
    def __init__(self, serializer, instance):
        self._serializer = serializer
        self._data = serializer.validated_data
        self._instance = instance

    def execute(self):
        self.is_valid()
        self._factory()
        return self._instance

    def _factory(self):
        raise_errors_on_nested_writes('update', self._serializer, self._data)
        update(instance=self._instance, data=self._data)


class DeleteUseCase(BaseUseCase):

    def __init__(self, instance):
        self._instance = instance

    def execute(self):
        self.is_valid()
        self._factory()
        return self._instance

    def _factory(self):
        self._instance.delete()


