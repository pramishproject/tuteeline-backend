from datetime import  datetime
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.core.usecases import BaseUseCase
from apps.staff.exceptions import StaffNotFound
from apps.staff.models import StaffPosition
from apps.staff import serializers


class AddStaffPositionUseCase(BaseUseCase):
    """
    use this to add staff position
    """

    def __init__(self,
                 serializer: serializers.AddStaffPositionSerializer):
        self.serializer = serializer
        self.data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        self._staff_position = StaffPosition(**self.data)
        self._staff_position.save()


class ListStaffPositionUseCase(BaseUseCase):
    """
    use this to list all staff position
    """

    def execute(self):
        self._factory()
        return self._staff_position

    def _factory(self):
        self._staff_position = StaffPosition.objects.unarchived()


class GetStaffPositionUseCase(BaseUseCase):
    def __init__(self, staff_position_id):
        self._staff_position_id = staff_position_id

    def execute(self):
        self._factory()
        return self._bus_company

    def _factory(self):
        try:
            self._bus_company = StaffPosition.objects.get(pk=self._staff_position_id)
        except StaffPosition.DoesNotExist:
            raise StaffNotFound


class UpdateStaffPositionUseCase(BaseUseCase):
    """
    use this to update staff position
    """

    def __init__(self, serializer: serializers.UpdateStaffPositionSerializer,
                 staff_position: StaffPosition):
        self.serializer = serializer
        self._data = serializer.validated_data
        self._staff_position = staff_position

    def execute(self):
        self._factory()

    def _factory(self):
        for key in self._data.keys():
            setattr(self._staff_position, key, self._data.get(key))
        self._staff_position.updated_at = datetime.now()
        self._staff_position.save()


class DeleteStaffPositionUseCase(BaseUseCase):
    def __init__(self, staff_position: StaffPosition):
        self._staff_position = staff_position

    def execute(self):
        self._factory()

    def _factory(self):
        self._staff_position.delete()
