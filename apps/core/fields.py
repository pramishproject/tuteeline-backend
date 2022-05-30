from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from apps.core import validators, form_fields


class PhoneNumberField(CharField):
    default_validators = [validators.validate_phone_number]
    description = _("Phone Number")

    def __init__(self, *args, **kwargs):
        # max_length=254 to be compliant with RFCs 3696 and 5321
        kwargs.setdefault('max_length', 20)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        # As with CharField, this will cause phone number validation to be performed
        # twice.
        return super().formfield(**{
            'form_class': form_fields.PhoneNumberField,
            **kwargs,
        })


class PasswordField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs.setdefault('style', {})
        kwargs['style']['input_type'] = 'password'
        kwargs['write_only'] = True

        super().__init__(**kwargs)
