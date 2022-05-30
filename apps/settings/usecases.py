from datetime import datetime

from apps.core.usecases import BaseUseCase
from apps.settings.exceptions import SettingsNotFound
from apps.settings.models import Settings


class AddColorUseCase(BaseUseCase):
    def __init__(self,serializer):
        self._serializer = serializer
        self._data = serializer.data

    def execute(self):
        self._factory()

    def _factory(self):
        self.settings = Settings(
            **self._data
        )
        self.settings.save()


class ListSettingColorUseCase(BaseUseCase):
    def execute(self):
        self._factory()
        return self._color

    def _factory(self):
        self._color = Settings.objects.all()




class GetSettingUseCase:
    def __init__(self, setting_id):
        self._setting_id = setting_id

    def execute(self):
        self._factory()
        return self._bus_company

    def _factory(self):
        try:
            self._bus_company = Settings.objects.get(pk=self._setting_id)
        except Settings.DoesNotExist:
            raise SettingsNotFound


class UpdateSettingColorUseCase(BaseUseCase):
    """
    use this to update staff position
    """

    def __init__(self, serializer,
                 setting:Settings):
        self.serializer = serializer
        self._data = serializer.validated_data
        self._setting = setting

    def execute(self):
        self._factory()

    def _factory(self):
        for key in self._data.keys():
            setattr(self._setting, key, self._data.get(key))
        self._setting.updated_at = datetime.now()
        self._setting.save()


