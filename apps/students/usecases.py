from apps.students.email import SendEmailToStudent
from datetime import datetime
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.notification.mixins import NotificationMixin
from apps.students.models import FavouriteInstitute, InstituteViewers, StudentAddress, StudentUser, StudentModel, CompleteProfileTracker
from apps.core import usecases
from apps.settings.models import Settings
from apps.core.usecases import BaseUseCase
from apps.students.exceptions import FavouriteInstituteNotFound, StudentAddressUnique, StudentModelNotFound


class RegisterStudentUseCase(usecases.CreateUseCase, NotificationMixin):
    notification_group = ['portal_user']

    def execute(self):
        super(RegisterStudentUseCase, self).execute()
        self.send_notification()

    def _factory(self):
        # 1. create student user
   
        user = StudentUser.objects.create(
            email=self._data.pop('email'),
            password=self._data.pop('password'),
            fullname=self._data.get('fullname')
        )
        # 2. Student
        self._student = StudentModel.objects.create(
            user=user,
            **self._data
        )

        Settings.objects.create(user=user)
        # SendEmailToStudent(
        #     context={
        #         'uuid': user.id,
        #         'name': user.fullname
        #     }
        # ).send(to=[user.email])

    def get_notification_data(self):
        return {
            'name': 'Student Registered',
            'image': self._student.image.url,
            'content': 'Student: {} Registered.'.format(self._student.fullname),
            'id': str(self._student.id)
        }

class GetStudentUseCase(BaseUseCase):
    def __init__(self,student_id:str):
        self._student_id =student_id

    def execute(self):
        self._factory()
        return self._student

    def _factory(self):
        try:
            self._student = StudentModel.objects.get(pk=self._student_id)

        except StudentModel.DoesNotExist:
            raise StudentModelNotFound

class GetFavouriteByIdUseCase(BaseUseCase):
    def __init__(self,favourite_id):
        self._favourite = favourite_id

    def execute(self):
        self._factory()
        return self._favourite_institute

    def _factory(self):
        try:
            self._favourite_institute = FavouriteInstitute.objects.get(pk=self._favourite)

        except FavouriteInstitute.DoesNotExist:
            raise FavouriteInstituteNotFound


class AddStudentAddressUseCase(usecases.CreateUseCase,GetStudentUseCase):
    def __init__(self, serializer,student_id:str):
        self._student_id= student_id
        super().__init__(serializer)

    def execute(self):
        self._factory()

    def _factory(self):
        # add student address

        StudentAddress.objects.create(
                **self._data,
                student=self._student_id
            )

        # get complete profile indicator
        try:
            complete_profile_indicator=CompleteProfileTracker.objects.get(student=self._student_id).update(complete_address = True)

        except CompleteProfileTracker.DoesNotExist:
             CompleteProfileTracker.objects.create(
                 student=self._student_id,
                 complete_address = True
             )
        

        # complete profile update




class GetStudentUserUseCase(BaseUseCase):
    def __init__(self,student):
        self._student_id =student

    def execute(self):
        self._factory()
        return self._student

    def _factory(self):
        try:
            
            student = StudentModel.objects.get(id=self._student_id)

            self._student = {'student': student}
        except StudentModel.DoesNotExist:
            raise StudentModelNotFound

class UpdateStudentUseCase(BaseUseCase):
    def __init__(self,serializer,student:StudentModel):
        self._student = student
        self._serializer = serializer
        self._data = self._serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        
        for data in self._data.keys():
            setattr(self._student,data,self._data[data])

        self._student.updated_at = timezone.now()
        self._student.save()
        user = self._student.user
        user.fullname = self._data.pop('fullname')
        user.updated_at = timezone.now()
        user.save()


class UpdateProfilePictureUseCase(BaseUseCase):
    def __init__(self,serializer,student:StudentModel):
        self._student = student
        self._serializer = serializer
        self._data = self._serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        for data in self._data.keys():
            setattr(self._student,data,self._data[data])
        self._student.updated_at = timezone.now()
        self._student.save()

class StudentAddressUpdateUseCase(BaseUseCase):
    def __init__(self,serializer,address:StudentAddress):
        self._address = address
        self._serializer = serializer
        self._data = self._serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        for key in self._data.keys():
            setattr(self._address,key,self._data.get(key))
        self._address.updated_at = datetime.now()
        self._address.save()
class StudentLatitudeLongitudeUpdateUseCase(BaseUseCase):
    def __init__(self,serializer,student:StudentModel):
        self._student = student
        self._serializer = serializer
        self._data = self._serializer.validated_data
    def execute(self):
        self._factory()

    def _factory(self):
        for key in self._data.keys():
            setattr(self._student,key,self._data.get(key))

        self._student.updated_at = datetime.now()
        self._student.save()

class GetAddressUseCase(BaseUseCase):
    def __init__(self,student_id:str):
        self._student_id =student_id
        # self._address_id = address_id

    def execute(self):
        self._factory()
        return self._student

    def _factory(self):
        try:
            self._student = StudentAddress.objects.get(student=self._student_id)

        except StudentModel.DoesNotExist:
            raise StudentModelNotFound

class GetStudentAddressUseCase(BaseUseCase):
    def __init__(self,address:StudentAddress):
        self._address =address

    def execute(self):
        self._factory()
        return self._student_address

    def _factory(self):
        try:
            self._student_address = StudentAddress.objects.get(pk=self._address)

        except StudentModel.DoesNotExist:
            raise StudentModelNotFound


class AddFavourateInstituteUseCase(BaseUseCase):
    def __init__(self , student:StudentModel ,serializer):
        self._student = student
        self._serializer = serializer
        self._data = self._serializer.validated_data
    def execute(self):
        self._factory()

    def _factory(self):
        FavouriteInstitute.objects.create(
                student = self._student,
                **self._data
            )

class GetFavouriteInstituteUseCase(BaseUseCase):
    def __init__(self , student:StudentModel):

        self._student = student

    def execute(self):
        self._factory()
        return self._favourite

    def _factory(self):
        self._favourite = FavouriteInstitute.objects.filter(
            student = self._student
        )

class DeleteFavouriteInstitute(BaseUseCase):
    def __init__(self , favourite):
        self._favourite = favourite

    def execute(self):
        self._factory()

    def _factory(self):
        self._favourite.delete()

class CreateInstituteViewersUseCase(BaseUseCase):
    def __init__(self,student,serializer):
        self._student = student
        self._serializer = serializer
        self._data= self._serializer.validated_data

    def execute(self):
        self._factory()
    
    def _factory(self):
        InstituteViewers.objects.create(
            student=self._student,
            **self._data
        )


class GetStudentHistryUseCase(BaseUseCase):
    def __init__(self,student):
        self._student = student

    def execute(self):
        self._factory()
        return self._visitor

    def _factory(self):
        self._visitor = InstituteViewers.objects.filter(student= self._student)
