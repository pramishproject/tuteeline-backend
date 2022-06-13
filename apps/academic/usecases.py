from apps.academic.exceptions import AcademicNotFound, EssayNotFound, LorNotFound, SopNotFound
from apps import students
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.core import usecases
from apps.core.usecases import BaseUseCase
from apps.academic.models import Academic, PersonalEssay, StudentLor, StudentSop
from apps.students.models import CompleteProfileTracker, StudentModel

class CreateStudentAcademicUseCase(usecases.CreateUseCase):
    def __init__(self, serializer,student):
        self._student = student
        super().__init__(serializer)

    def execute(self):
        self._factory()

    def _factory(self):
        #1. create Academic
        try:
            self._academic=Academic.objects.create(
                student=self._student,
                **self._data
            )
        except Academic.validate_unique:
            raise
        try:
            complete_profile=CompleteProfileTracker.objects.get(student=self._student)
            complete_profile.complete_academic_detail=True
            complete_profile.save()
        except CompleteProfileTracker.DoesNotExist:
            CompleteProfileTracker.objects.create(
                student=self._student,
                complete_academic_detail=True) 

class GetStudentAcademicUseCase(BaseUseCase):

    def __init__(self,academic_id):
        self._academic_id = academic_id

    def execute(self):
        self._factory()
        return self._academic

    def _factory(self):
        try:
            self._academic=Academic.objects.get(pk=self._academic_id)
        except Academic.DoesNotExist:
            raise AcademicNotFound


class UpdateAcademicUseCase(BaseUseCase):
    def __init__(self,serializer,academic:Academic):
        self._academic=academic
        self._serializer = serializer
        self._data = self._serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        for data in self._data.keys():
            setattr(self._academic,data,self._data[data])

        self._academic.updated_at = timezone.now()
        self._academic.save()

class UpdateSopUseCase(BaseUseCase):
    def __init__(self,serializer,id:StudentSop):
        self._id = id
        self._serializer = serializer
        self._data = self._serializer.validated_data
    
    def execute(self):
        self._factory()

    def _factory(self):
        for data in self._data.keys():
            setattr(self._id,data, self._data[data])
        
        self._id.updated_at = timezone.now()
        self._id.save()

        
class GetAcademicListUseCase(BaseUseCase):
    def __init__(self,student):
        self._student = student

    def execute(self):
        self._academic = Academic.objects.filter(student=self._student)      
        return self._academic

        
class GetSopByIdUseCase(BaseUseCase):
    def __init__(self,id):
        self._sop_id = id
    
    def execute(self):
        self._factory()
        return self._sop
    
    def _factory(self):
        try:

            self._sop = StudentSop.objects.get(id= self._sop_id)

        except StudentSop.DoesNotExist:
            raise SopNotFound 

class CreateStudentSopUseCase(usecases.CreateUseCase):
    def __init__(self, serializer ,student):
        self._student = student
        super().__init__(serializer)

    def execute(self):
        self._factory()

    def _factory(self):
        #1. create Sop
        
        self._academic=StudentSop.objects.create(
            student=self._student,
            **self._data
        )
        try:
            complete_profile=CompleteProfileTracker.objects.get(student=self._student)
            complete_profile.complete_sop_field=True
            complete_profile.save()
        except CompleteProfileTracker.DoesNotExist:
            CompleteProfileTracker.objects.create(
                student=self._student,
                complete_sop_field=True) 


class GetSopUseCase(BaseUseCase):
    def __init__(self,student):
        self._student_id = student

    def execute(self):
        
        self._factory()
        return self._sop

    def _factory(self):
        try:
            self._sop=StudentSop.objects.get(student=self._student_id)
        except StudentSop.DoesNotExist:
            raise SopNotFound


class GetLorUseCase(BaseUseCase):
    def __init__(self,student):
        self._student_id = student

    def execute(self):
        
        self._factory()
        return self._lor

    def _factory(self):
        try:
            self._lor=StudentLor.objects.get(student=self._student_id)
        except StudentLor.DoesNotExist:
            raise LorNotFound



class GetLorListUseCase(BaseUseCase):
    def __init__(self,student):
        self._student = student

    def execute(self):
        self._lor=StudentLor.objects.filter(student=self._student)
        return self._lor

class GetStudentSopUseCase(BaseUseCase):
    def __init__(self,student):
        
        self._student = student

    def execute(self):
        
        self._factory()
        return self._sop

    def _factory(self):
        try:
            self._sop=StudentSop.objects.filter(student=self._student)
        except StudentSop.DoesNotExist:
            raise SopNotFound

class CreateStudentLorUseCase(usecases.CreateUseCase):
    def __init__(self, serializer ,student):
        self._student = student
        super().__init__(serializer)

    def execute(self):
        self._factory()

    def _factory(self):
        #1. create student lor
        self._academic=StudentLor.objects.create(
            student=self._student,
            **self._data
        )
        try:
            complete_profile=CompleteProfileTracker.objects.get(student=self._student)
            complete_profile.complete_lor_field=True
            complete_profile.save()
        except CompleteProfileTracker.DoesNotExist:
            CompleteProfileTracker.objects.create(
                student=self._student,
                complete_lor_field=True) 



class CreateStudentEssayUseCase(usecases.CreateUseCase):
    def __init__(self, serializer ,student):
        self._student = student
        super().__init__(serializer)

    def execute(self):
        self._factory()

    def _factory(self):
        #1. create personal essay
        self._academic=PersonalEssay.objects.create(
            student=self._student,
            **self._data
        )
        try:
            complete_profile=CompleteProfileTracker.objects.get(student=self._student)
            complete_profile.complete_personalessay_field=True
            complete_profile.save()
        except CompleteProfileTracker.DoesNotExist:
            CompleteProfileTracker.objects.create(
                student=self._student,
                complete_personalessay_field=True) 


class GetEssayUseCase(BaseUseCase):
    def __init__(self,student_id):
        self._student_id = student_id

    def execute(self):
        self._factory()
        return self._essay

    def _factory(self):
        try:
            self._essay= PersonalEssay.objects.get(student=self._student_id)
        except PersonalEssay.DoesNotExist:
            raise EssayNotFound

class GetEssayByIdUseCase(BaseUseCase):
    def __init__(self,essay_id):
        self._essay_id = essay_id
    def execute(self):
        self._factory()
        return self._essay
    
    def _factory(self):
        try:
            self._essay= PersonalEssay.objects.get(id=self._essay_id)
        except PersonalEssay.DoesNotExist:
            raise EssayNotFound
class GetPersonalEssayUseCase(BaseUseCase):
    def __init__(self,student):
        self._student = student

    def execute(self):
        self._factory()
        return self._personal_essay

    def _factory(self):
        try:
            self._personal_essay= PersonalEssay.objects.filter(student=self._student)
        except PersonalEssay.DoesNotExist:
            raise EssayNotFound

class DeleteSopUseCase(BaseUseCase):
    def __init__(self,sop):
        self._sop = sop
    
    def execute(self):
        self._factory()

    def _factory(self):
        self._sop.delete()

class UpdateEssayUseCase(BaseUseCase):
    def __init__(self,serializer,essay:PersonalEssay):
        self._essay = essay
        self._serializer = serializer
        self._data = self._serializer.validated_data
    
    def execute(self):
        self._factory()

    def _factory(self):
        for data in self._data.keys():
            setattr(self._essay,data, self._data[data])
        
        self._essay.updated_at = timezone.now()
        self._essay.save()

class DeleteEssayUseCase(BaseUseCase):
    def __init__(self,essay):
        self._essay = essay
    
    def execute(self):
        self._factory()

    def _factory(self):
        self._essay.delete()


class DeleteAcademicUseCase(BaseUseCase):
    def __init__(self,academic):
        self._academic = academic
    
    def execute(self):
        self._factory()

    def _factory(self):
        self._academic.delete()