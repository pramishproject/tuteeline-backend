from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.core.usecases import BaseUseCase
from apps.notification.mixins import NotificationMixin
from apps.troubleshooting.exceptions import TroubleshootNotFound
from apps.troubleshooting.models import BillingTroubleshoot, Troubleshoot


class AddTroubleShootTicketUseCase(BaseUseCase, NotificationMixin):
    notification_group = ['portal_user']

    def __init__(self, serializer, consultancy_user):
        self._serializer = serializer
        self._consultancy_user = consultancy_user
        self._data = serializer.validated_data

    def execute(self):
        self._factory()
        self.send_notification()

    def _factory(self):
        self._troubleshot = Troubleshoot(
            description=self._data['description'],
            status='RECEIVED',
            troubleshoot_type=self._data['troubleshoot_type']
        )
        self._troubleshot.save()
        if self._data['troubleshoot_type'] == 'BILLING':
            billing_troubleshoot = BillingTroubleshoot(
                trouble_shot=self._troubleshot,
                type=self._data['type'],
                category=self._data['category'],
                subject=self._data['subject']
            )
            try:
                billing_troubleshoot.clean()
            except DjangoValidationError as e:
                raise ValidationError(e.message_dict)
            billing_troubleshoot.save()

    def get_notification_data(self):
        return {
            'name': 'Troubleshoot Received',
            'image': self._consultancy_user.consultancy.logo.url,
            'content': 'Troubleshoot Received from: {}.'.format(self._consultancy_user.consultancy.name),
            'id': str(self._troubleshot.id)
        }


class GetTroubleshootUseCase(BaseUseCase):
    def __init__(self, troubleshoot_id: Troubleshoot):
        self._troubleshoot_id = troubleshoot_id

    def execute(self):
        self._factory()
        return self.troubleshot

    def _factory(self):
        try:
            self.troubleshot = Troubleshoot.objects.get(pk=self._troubleshoot_id)
        except Troubleshoot.DoesNotExist:
            raise TroubleshootNotFound


class ListTroubleShootTicketUseCases(BaseUseCase):
    def execute(self):
        self._factory()
        return self._trouble_shoot

    def _factory(self):
        self._trouble_shoot = Troubleshoot.objects.all()


class UpdateTroubleShootUseCase(BaseUseCase):
    def __init__(self, serializer, troubleshoot: Troubleshoot):
        self._troubleshoot = troubleshoot
        self._serializer = serializer
        self._data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        for data in self._data.keys():
            setattr(self._troubleshoot, data, self._data[data])
        self._troubleshoot.updated_at = timezone.now()
        self._troubleshoot.save()
