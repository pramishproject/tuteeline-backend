from django.core.exceptions import ValidationError
from django.core.validators import _lazy_re_compile
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class Validator:
    message = None
    code = 'invalid'

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        raise NotImplementedError("Subclasses should implement this!")

    def __eq__(self, other):
        return (
                isinstance(other, Validator) and
                (self.message == other.message) and
                (self.code == other.code)
        )


@deconstructible
class WordValidator(Validator):
    message = _('Enter a valid word.')
    number_of_word = None
    word_length = 2
    one_word_regex = _lazy_re_compile(
        r'^[aA-zZ]+$'
    )
    multi_word_regex = _lazy_re_compile(
        r'^[aA-zZ\s]+$'
    )

    def __call__(self, value):
        """
        raise on:
        1. empty value
        2. not matched to regex
        3. if has a word less than 2 character
        """
        if not value:
            raise ValidationError(self.message, code=self.code)

        if self.number_of_word == 1:
            self._match_regex(regex=self.one_word_regex, value=value)
            self._check_word_length(value=value)
        else:
            self._match_regex(regex=self.multi_word_regex, value=value)

            split_word = value.split(' ')

            if len(split_word) > self.number_of_word:
                raise ValidationError(self.message, code=self.code)

            for name in split_word:
                self._check_word_length(value=name)

    def _check_word_length(self, value):
        if _lazy_re_compile(r'^[aA-zZ]+$').match(value):
            if len(value) < self.word_length:
                raise ValidationError(self.message, code=self.code)

    def _match_regex(self, regex, value):
        if not regex.match(value):
            raise ValidationError(self.message, code=self.code)


@deconstructible
class PhoneNumberValidator(Validator):
    message = _('Enter a valid phone number.')
    phone_number_regex = _lazy_re_compile(r'^[0-9/+/-]+$')

    def __call__(self, value):
        if not value:
            raise ValidationError(self.message, code=self.code)

        if not self.phone_number_regex.match(value):
            raise ValidationError(self.message, code=self.code)


@deconstructible
class ImageValidator(Validator):
    message = _('The maximum image file size that can be uploaded is 8MB')
    file_size = 8194304

    def __call__(self, value):
        if not value:
            raise ValidationError(self.message, code=self.code)

        if value.size > self.file_size:
            raise ValidationError(self.message, code=self.code)


@deconstructible
class NonZeroIntegerValidator(Validator):
    message = _('Enter a valid integer.')

    def __call__(self, value):
        if not value:
            raise ValidationError(self.message, code=self.code)

        if value == 0:
            raise ValidationError(_('Integer can\'t be zero.'), code=self.code)


validate_phone_number = PhoneNumberValidator()
validate_image = ImageValidator()
validate_non_zero_integer = NonZeroIntegerValidator()
