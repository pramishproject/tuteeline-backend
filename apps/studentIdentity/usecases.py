from apps.studentIdentity.exceptions import CitizenshipNotFound, PassportNotFound
from apps.core.models import BaseModel
from apps.students.models import CompleteProfileTracker, StudentModel
from apps.studentIdentity.models import Citizenship, Passport
from django.utils.datetime_safe import datetime
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from apps.core.usecases import BaseUseCase


class AddCitizenshipUseCase(BaseUseCase):
    def __init__(self , serializer ,student_id:str):
        self.serializer = serializer
        self._student_id =student_id
        self.data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        self._citizenship = Citizenship(
            **self.data,
            student = self._student_id
        )
        self._citizenship.save()

        try:
            complete_profile_indicator=CompleteProfileTracker.objects.get(student=self._student_id)
            complete_profile_indicator.complete_citizenship_detail=True
            complete_profile_indicator.save()

        except CompleteProfileTracker.DoesNotExist:
            CompleteProfileTracker.objects.create(
                student=self._student_id,
                complete_citizenship_detail=True
            )


class AddPassportUseCase(BaseUseCase):
    def __init__(self , student_id:StudentModel,serializer):
        self.serializer = serializer
        self._student_id =student_id
        self.data = serializer.validated_data

    def execute(self):
        print("********************************jhsdgfjhsstudent",self._student_id)
        self._factory()

    def _factory(self):
        self._passport = Passport(
            student = self._student_id,
            **self.data,
        )
        self._passport.save()
        try:
            complete_profile_indicator=CompleteProfileTracker.objects.get(student=self._student_id)
            complete_profile_indicator.complete_passport_field=True
            complete_profile_indicator.save()

        except CompleteProfileTracker.DoesNotExist:
            CompleteProfileTracker.objects.create(
                student=self._student_id,
                complete_passport_field=True
            )


class GetCitizenshipUseCase(BaseUseCase):
    def __init__(self,student_id):
        self._student = student_id

    def execute(self):
        self._factory()
        return self._citizenship

    def _factory(self):
        try:
            self._citizenship = Citizenship.objects.get(student=self._student)
        except Citizenship.DoesNotExist:
            raise CitizenshipNotFound

class GetStudentCitizenshipUseCase(BaseUseCase):
    def __init__(self,citizenship):
        self._citizenship_id= citizenship

    def execute(self):
        self._factory()
        return self._citizenship
    def _factory(self):
        try:
            self._citizenship = Citizenship.objects.get(pk=self._citizenship_id)
        except Citizenship.DoesNotExist:
            raise CitizenshipNotFound
    

class GetPassportUseCase(BaseUseCase):
    def __init__(self,student_id):
        self._student = student_id

    def execute(self):
        self._factory()
        print("***************************inpassget")
        return self._passport

    def _factory(self):
        try:
            self._passport = Passport.objects.get(student=self._student)
        except Passport.DoesNotExist:
            raise PassportNotFound


class GetStudentPassportUseCase(BaseUseCase):
    def __init__(self,passport):
        self._passport_id= passport

    def execute(self):
        self._factory()
        return self._pasport
    def _factory(self):
        try:
            self._pasport = Passport.objects.get(pk=self._passport_id)
        except Passport.DoesNotExist:
            raise PassportNotFound


class UpdateCitizenshipUseCase(BaseUseCase):
    def __init__(self,serializer,citizenship: Citizenship):
        self._citizenship = citizenship
        self._serializer = serializer
        self._data = self._serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        for data in self._data.keys():
            setattr(self._citizenship,data,self._data[data])
        self._citizenship.updated_at = timezone.now()
        self._citizenship.save()

class UpdatePassportUseCase(BaseUseCase):
    def __init__(self,serializer,passport:Passport):
        self._passport = passport
        self._serializer = serializer
        self._data = self._serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        for data in self._data.keys():
            setattr(self._passport,data,self._data[data])
        self._passport.updated_at = timezone.now()
        self._passport.save()


