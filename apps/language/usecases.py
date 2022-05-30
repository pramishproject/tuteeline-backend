from apps.language.exceptions import LanguageNotFound
from apps.language.models import Language
from datetime import datetime
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.core import usecases
from apps.settings.models import Settings
from apps.core.usecases import BaseUseCase

class CreateLanguageUseCase(BaseUseCase):

    def __init__(self,student,serializer):
        self._student = student
        self._data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        Language.objects.create(
            student= self._student,
             **self._data,
        )

class GetLanguageUseCase(BaseUseCase):
    def __init__(self,language_id:str):
        self._language_id = language_id

    def execute(self):
        self._factory()
        return self._language

    def _factory(self):
        try:
            self._language = Language.objects.get(pk = self._language_id)
        except Language.DoesNotExist:
            raise LanguageNotFound


class GetStudentLanguageUsecase(BaseUseCase):
    def __init__(self,student):
        self._student =student

    def execute(self):
        self._factory()
        return self._language

    def _factory(self):
        self._language = Language.objects.filter(student= self._student)
    

class UpdateStudentLanguageUseCase(BaseUseCase):
    def __init__(self,language,serializer):
        self._language = language
        self._serializer = serializer
        self._data = self._serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        for data in self._data.keys():
            setattr(self._language, data, self._data[data])
        self._language.updated_at = timezone.now()
        self._language.save()

class DeleteLanguageUseCase(BaseUseCase):
    def __init__(self,language):
        self._language = language
    
    def execute(self):
        self._factory()

    def _factory(self):
        self._language.delete()