from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.consultancy import tasks
from apps.consultancy.emails import SendEmailToConsultanySTaff
from apps.consultancy.exceptions import ConsultancyNotFound, ConsultancyStaffNotFound
from apps.consultancy.models import Consultancy, ConsultancyStaff
from apps.core import usecases
from apps.core.usecases import BaseUseCase
from apps.notification.mixins import NotificationMixin
from apps.settings.models import Settings
from apps.staff.models import StaffPosition
from apps.user.models import ConsultancyUser


class RegisterConsultancyUseCase(usecases.CreateUseCase, NotificationMixin):
    notification_group = ['portal_user']

    def execute(self):
        super(RegisterConsultancyUseCase, self).execute()
        self.send_notification()

    def _factory(self):
        # 1. create consultancy user
        user = ConsultancyUser.objects.create(
            email=self._data.pop('email'),
            password=(self._data.pop('password'))
        )
        # 2. consultancy
        self._consultancy = Consultancy.objects.create(
            **self._data
        )
        role, created = StaffPosition.objects.get_or_create(name='owner')

        Settings.objects.create(user=user)
        # 3. consultancy staff
        ConsultancyStaff.objects.create(
            user=user,
            consultancy=self._consultancy,
            role=role
        )

    def get_notification_data(self):
        return {
            'name': 'Consultancy Registered',
            'image': self._consultancy.logo.url,
            'content': 'Consultancy: {} Registered.'.format(self._consultancy.name),
            'id': str(self._consultancy.id)
        }


class GetConsultancyUseCase(BaseUseCase):
    def __init__(self, consultancy_id: Consultancy):
        self._consultancy_id = consultancy_id
    # def __init__(self, consultancy_id):
    #     self._consultancy_id = consultancy_id

    def execute(self):
        self._factory()
        return self._consultancy

    def _factory(self):
        try:
            self._consultancy = Consultancy.objects.get(pk=self._consultancy_id)
        except Consultancy.DoesNotExist:
            raise ConsultancyNotFound


class GetConsultancyStaffUseCase(BaseUseCase):
    def __init__(self, consultancy_staff_id: ConsultancyStaff):
        self._consultancy_staff_id = consultancy_staff_id

    def execute(self):
        self._factory()
        return self.consultancy_staff

    def _factory(self):
        try:
            print(self._consultancy_staff_id)
            self.consultancy_staff = ConsultancyStaff.objects.get(pk=self._consultancy_staff_id)
        except ConsultancyStaff.DoesNotExist:
            raise ConsultancyStaffNotFound


class CreateConsultancyStaffUseCase(usecases.CreateUseCase):
    def __init__(self, serializer, consultancy: Consultancy):
        self._consultancy = consultancy
        super().__init__(serializer)

    def execute(self):
        self._factory()

    def _factory(self):
        user = {
            'email': self._data.pop('email'),
            'fullname': self._data.pop('fullname'),
        }
        # 1. create consultancy user
        self.consultancy_user = ConsultancyUser.objects.create(
            **user
        )
        Settings.objects.create(user=self.consultancy_user)
        # 2. consultancy staff
        try:
            consultancy_staff = ConsultancyStaff.objects.create(
                user=self.consultancy_user,
                consultancy=self._consultancy,
                role=self._data['role'],
                profile_photo=self._data['profile_photo']
            )
            consultancy_staff.clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)
        context = {
            'uuid': self.consultancy_user.id,
            'name': self._consultancy.name,
            'user_email':self.consultancy_user.email,
        }
        # tasks.send_set_password_email_to_user.apply_async(
        #     kwargs=context
        # )

        # without celery
        SendEmailToConsultanySTaff(
            context={
                'uuid': self.consultancy_user.id,
                'name': self._consultancy.name
            }
        ).send(to=[self.consultancy_user.email])




class UpdateConsultancyStaffUseCase(BaseUseCase):
    def __init__(self, serializer, consultancy_staff: ConsultancyStaff):
        self._consultancy_staff = consultancy_staff
        self._serializer = serializer
        self._data = self._serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        fullname = self._data.pop('fullname')
        for data in self._data.keys():
            setattr(self._consultancy_staff, data, self._data[data])
        self._consultancy_staff.updated_at = timezone.now()
        self._consultancy_staff.save()
        user = self._consultancy_staff.user
        user.fullname = fullname
        user.updated_at = timezone.now()
        user.save()


class ListConsultancyStaffUseCase(BaseUseCase):
    def __init__(self, consultancy: Consultancy):
        self._consultancy = consultancy

    def execute(self):
        self._factory()
        return self._consultancy_staff

    def _factory(self):
        self._consultancy_staff = ConsultancyStaff.objects.filter(consultancy=self._consultancy)


class ListConsultancyUseCase(BaseUseCase):
    def execute(self):
        self._factory()
        return self._consultancy

    def _factory(self):
        self._consultancy = Consultancy.objects.all()


class UpdateConsultancyStaffPhotoUseCase(BaseUseCase):
    def __init__(self, serializer, consultancy_staff: ConsultancyStaff):
        self._consultancy_staff = consultancy_staff
        self._serializer = serializer
        self._data = self._serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        for data in self._data.keys():
            setattr(self._consultancy_staff, data, self._data[data])
        self._consultancy_staff.updated_at = timezone.now()
        self._consultancy_staff.save()


class DeactivateConsultancyUserUseCase(BaseUseCase):
    def __init__(self, serializer, consultancy_user):
        self._serializer = serializer
        self._data = serializer.validated_data
        self._consultancy_user = consultancy_user

    def execute(self):
        self.is_valid()
        self._factory()

    def _factory(self):
        self._consultancy_user.deactivate_user()

    def is_valid(self):
        if self._data['is_active']:
            raise ValidationError({
                'is_active': _("User is already deactivated.")
            })


class ActivateConsultancyUserUseCase(BaseUseCase):
    def __init__(self, serializer, consultancy_user):
        self._serializer = serializer
        self._data = serializer.validated_data
        self._consultancy_user = consultancy_user

    def execute(self):
        self.is_valid()
        self._factory()

    def _factory(self):
        self._consultancy_user.activate_user()

    def is_valid(self):
        if not self._data['is_active']:
            raise ValidationError({
                'is_active': _("User is already activated.")
            })

class UpdateConsultancyUseCase(BaseUseCase):
    def __init__(self,instance,serializer):
        self._instance = instance
        self._serializer = serializer
        self._data = self._serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        for data in self._data.keys():
            setattr(self._instance, data, self._data[data])
        self._instance.updated_at = timezone.now()
        self._instance.save()