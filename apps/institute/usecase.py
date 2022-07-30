
from datetime import datetime
from apps.institute.exceptions import FacilityDoesntExist, InstituteNotFound,\
    InstituteScholorshipDoesntExist, SocialMediaLinkDoesntExist,StaffNotFound

from apps.staff.models import INSTITUTE_PERMISSIONS
from apps.staff.models import StaffPosition
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework.exceptions import ValidationError

from apps.core import usecases
from apps.core.usecases import BaseUseCase, BaseUserUseCase
from apps.notification.mixins import NotificationMixin
from apps.institute.models import (AddInstituteFacility, 
                                   Facility, 
                                   Institute, 
                                   InstituteScholorship, 
                                   InstituteStaff,
                                   InstituteUser, 
                                   SocialMediaLink)
from apps.settings.models import Settings

class RegisterInstituteUsecase(usecases.CreateUseCase, NotificationMixin):
    notification_group = ['portel_user']

    def execute(self):
        super(RegisterInstituteUsecase, self).execute()
        self.send_notification()

    def _factory(self):
        fullname = self._data.get("fullName")
        if fullname != None:
            self._data.pop("fullName")
        user = InstituteUser.objects.create(
            email=self._data.pop("email"),
            password=(self._data.pop("password")),
            fullname = fullname
        )

        #2. Institute
        self._institute =  Institute.objects.create(
            **self._data
        )
        role,created = StaffPosition.objects.\
            get_or_create(name='owner',
                        institute=self._institute,
                          permission_list=INSTITUTE_PERMISSIONS)

        Settings.objects.create(user=user)

        #3. institute staff
        InstituteStaff.objects.create(
            user=user,
            institute=self._institute,
            role=role
        )

    def get_notification_data(self):
        return {
            'name': 'Institute Registered',
            'image': self._institute.logo.url,
            'content': 'Institute: {} Registered.'.format(self._institute.name),
            'id': str(self._institute.id)
        }


            
class ListInstituteUseCase(BaseUseCase):
    def execute(self):
        self._factory()
        return self._institute

    def _factory(self):
        self._institute = Institute.objects.all().distinct()


class GetInstituteUseCase(BaseUseCase):
    def __init__(self,institute_id:str):
        self._institute_id = institute_id

    def execute(self):
        self._factory()
        return self._institute

    def _factory(self):
        try:
            self._institute = Institute.objects.get(pk=self._institute_id)
        except Institute.DoesNotExist:
            raise InstituteNotFound

class GetInstituteStaffUseCase(BaseUseCase):
    def __init__(self,institute_staff_id):
        self._staff_id = institute_staff_id

    def execute(self):
        self._factory()
        return self._staff

    def _factory(self):
        try:
            self._staff = InstituteStaff.objects.get(pk=self._staff_id)
        except InstituteStaff.DoesNotExist:
            raise StaffNotFound

class GetInstituteDetailUseCase(BaseUseCase):
    def __init__(self,institute_id:str):
        self._institute_id = institute_id

    def execute(self):
        self._factory()
        return self._institute

    def _factory(self):
        try:
            self._institute = Institute.objects.get(pk=self._institute_id)

        except Institute.DoesNotExist:
            raise InstituteNotFound

class UpdateInstituteUseCase(usecases.CreateUseCase):
    def __init__(self, institute,serializer):
        self._institute = institute
        self._data=serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        for key in self._data.keys():
            setattr(self._institute,key,self._data.get(key))

        self._institute.updated_at =datetime.now()
        self._institute.save()


class AddScholorshipUseCase(usecases.CreateUseCase):
    def __init__(self,serializer,institute):
        self._institute = institute
        self._data=serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        InstituteScholorship.objects.create(
            institute = self._institute,
            **self._data
        )
class GetScholorshipUseCase(BaseUseCase):
    def __init__(self,scholorship_id):
        self._scholorship_id = scholorship_id

    def execute(self):
        self._factory()
        return self._scholorship 
    
    def _factory(self):
        try:
            self._scholorship = InstituteScholorship.objects.get(pk=self._scholorship_id)

        except InstituteScholorship.DoesNotExist:
            raise InstituteScholorshipDoesntExist

class UpdateScholorshipUseCase(BaseUseCase):
    def __init__(self,serializer,scholorship: InstituteScholorship):
        self.serializer = serializer
        self._data = serializer.validated_data
        self._schlorship=scholorship

    def execute(self):
        self._factory()

    def _factory(self):
        for key in self._data.keys():
            setattr(self._schlorship,key,self._data.get(key))

        self._schlorship.updated_at =datetime.now()
        self._schlorship.save()


class ListScholorshipUseCase(BaseUseCase):
    def __init__(self,institute):
        self._institute = institute

    def execute(self):
        self._factory()
        return self._scholorship

    def _factory(self):
        self._scholorship = InstituteScholorship.objects.filter(institute = self._institute)


class DeleteScholorshipUseCase(BaseUseCase):
    def __init__(self,scholorship):
        self._scholorship = scholorship

    def execute(self):
        return self._factory()

    def _factory(self):
        self._scholorship.delete()

class DeleteFacilityUseCase(BaseUseCase):
    def __init__(self,facility):
        self._facility = facility

    def execute(self):
        return self._factory()

    def _factory(self):
        self._facility.delete()

class CreateInstituteStaffUseCase(BaseUseCase,BaseUserUseCase):
    def __init__(self,serializer,institute,request):
        self._institute = institute
        self._data = serializer.validated_data
        self._request = request
    def execute(self):
        self._factory()
        super()._send_email(self.institute_user, self._request,"verify")
    def _factory(self):
        user  = {
            'email':self._data.pop('email'),
            'fullname' : self._data.pop('fullname')
        }

        #1. create institute user
        self.institute_user = InstituteUser.objects.create(
            **user
        )
        Settings.objects.create(user = self.institute_user)

        #2 . institute staff
        try:
            consultancy_staff = InstituteStaff.objects.create(
                user=self.institute_user,
                institute=self._institute,
                role=self._data['role'],
                profile_photo=self._data['profile_photo']
            )
            consultancy_staff.clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)


        # send_to = os.getenv("DEFAULT_EMAIL", self.institute_user.email)
        # context = {
        #     'uuid': self.institute_user.id,
        #     'name': self.institute_user.name,
        #     'user_email':self.institute_user.email,
        # }
        # tasks.send_set_password_email_to_user.apply_async(
        #     kwargs=context
        # )

        # without celery

        # SendEmailToInstituteStaff(
        #     context={
        #         'uuid': self.institute_user.id,
        #         'name': self._institute.name
        #     }
        # ).send(to=[send_to])
    
class ListInstituteStaffUseCase(BaseUseCase):
    def __init__(self,institute):
        self._institute = institute

    def execute(self):
        self._factory()
        return self._staff

    def _factory(self):
        self._staff=InstituteStaff.objects.filter(institute = self._institute)

class SocialiMedialinkUseCase(usecases.CreateUseCase):

    def __init__(self,serializer,institute):
        self._institute = institute
        self._data=serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        SocialMediaLink.objects.create(
            institute = self._institute,
            **self._data
        )


class DeleteSocialMediaUseCase(BaseUseCase):
    def __init__(self,socialmedia):
        self._socialmedia = socialmedia

    def execute(self):
        return self._factory()

    def _factory(self):
        self._socialmedia.delete()

class GetSocialMedia(BaseUseCase):
    def __init__(self,socialmedia_id):
        self._socialmedia_id = socialmedia_id

    def execute(self):
        self._factory()
        return self._socialmedia_id 
    
    def _factory(self):
        try:
            self._socialmedia_id  = SocialMediaLink.objects.get(pk=self._socialmedia_id)

        except SocialMediaLink.DoesNotExist:
            raise SocialMediaLinkDoesntExist


class FacilityUseCase(BaseUseCase):
    def __init__(self,facility_id):
        self._facility_id = facility_id

    def execute(self):
        self._factory()
        return self._facility

    def _factory(self):
        try:
            self._facility=AddInstituteFacility.objects.get(pk=self._facility_id)
        except AddInstituteFacility.DoesNotExist:
            raise FacilityDoesntExist

class GetSocialMediaLinkListUseCase(BaseUseCase):
    def __init__(self,institute):
        self._institute = institute

    def execute(self):
        self._factory()
        return self._socialmedia

    def _factory(self):
        self._socialmedia=SocialMediaLink.objects.filter(institute=self._institute)


class CreateInstituteFacilityUseCase(BaseUseCase):
    def __init__(self,serializer,institute):
        self._data = serializer.validated_data
        self._institute = institute

    def execute(self):
        self._factory()

    def _factory(self):
        try:
            AddInstituteFacility.objects.create(
                facility=self._data.pop('facility'),
                institute = self._institute
            )
        except Facility.DoesNotExist:
            raise FacilityDoesntExist


class GetFacilityUseCase(BaseUseCase):
    def __init__(self,institute):
        self._institute = institute

    def execute(self):
        self._factory()
        return self._facility

    def _factory(self):
        self._facility = AddInstituteFacility.objects.filter(institute = self._institute)


class GetInstituteStaffDetailUseCase(BaseUseCase):
    def __init__(self,staff):
        self._staff = staff

    def execute(self):
        self._factory()
        return self._staff_detail
    def _factory(self):
        try:
            self._staff_detail = InstituteStaff.objects.get(pk=self._staff)

        except InstituteStaff.DoesNotExist:
            raise StaffNotFound


class InstituteStaffUpdate(BaseUseCase):
    def __init__(self, instance, serializer):
        self._instance = instance
        self._data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        fullname = self._data.pop('fullname')
        for key in self._data.keys():
            setattr(self._instance, key, self._data.get(key))

        self._instance.updated_at = datetime.now()
        self._instance.save()

        self.user = self._instance.user
        self.user.fullname = fullname
        self.user.updated_at = datetime.now()
        self.user.save()

class CustomInstituteUpdate(BaseUseCase):
    def __init__(self, instance, serializer):
        self._instance = instance
        self._data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        for key in self._data.keys():
            setattr(self._instance, key, self._data.get(key))

        self._instance.updated_at = datetime.now()
        self._instance.save()


class VerifyAndChangePasswordUseCase(BaseUseCase):
    # def __init__(self,user):
    #     self._user = user

    def execute(self):
        self._factory()

    def _factory(self):
        print(",fkdj")