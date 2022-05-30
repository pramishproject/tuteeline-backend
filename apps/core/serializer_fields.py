from django.utils.translation import gettext_lazy as _
from rest_framework.fields import CharField

from apps.core import validators


class PhoneNumberField(CharField):
    default_error_messages = {
        'invalid': _('Enter a valid phone number.')
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        validator = validators.PhoneNumberValidator(message=self.error_messages['invalid'])
        self.validators.append(validator)

