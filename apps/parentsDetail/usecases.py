from apps.parentsDetail.exceptions import ParentsNotFound
from datetime import datetime
from rest_framework import parsers
from apps.students.models import CompleteProfileTracker
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.core import usecases
from apps.core.usecases import BaseUseCase
from apps.parentsDetail.models import StudentParents

class AddParentsUseCase(usecases.CreateUseCase):
    def __init__(self, serializer ,student):
        self._student = student
        super().__init__(serializer)

    def execute(self):
        self._factory()

    def _factory(self):
        StudentParents.objects.create(
            student=self._student,
            **self._data
        )
        try:
            complete_profile_indicator=CompleteProfileTracker.objects.get(student=self._student)
            complete_profile_indicator.complete_parents_detail=True
            complete_profile_indicator.save()

        except CompleteProfileTracker.DoesNotExist:
            CompleteProfileTracker.objects.create(
                student=self._student,
                complete_parents_detail=True
            )


class GetParentsUseCase(BaseUseCase):
    def __init__(self,parents_id) :
        self._parents_id = parents_id

    def execute(self):
        self._factory()
        return self._parents

    def _factory(self):
        try:
            self._parents= StudentParents.objects.get(pk= self._parents_id)

        except StudentParents.DoesNotExist:
            raise ParentsNotFound


class UpdateParentsUseCase(BaseUseCase):
    def __init__(self, serializer,parents:StudentParents):
        self._parents = parents
        self.serializer = serializer
        self._data = serializer.validated_data
        

    def execute(self):
        self._factory()

    def _factory(self):
        for key in self._data.keys():
            setattr(self._parents,key,self._data.get(key))

        self._parents.updated_at = datetime.now()
        self._parents.save()

class DeleteParentsUseCase(BaseUseCase):
    def __init__(self,parents:StudentParents):
        self._parents = parents

    def execute(self):
        self._factory()

    def _factory(self):
        self._parents.delete()


class GetStudentParentsUseCase(BaseUseCase):
    def __init__(self,student):
        self._student = student

    def execute(self):
        self._parents= StudentParents.objects.filter(student=self._student)
        return self._parents