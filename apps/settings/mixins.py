from apps.settings.usecases import GetSettingUseCase


class SettingMixin:
    def get_setting(self):
        return GetSettingUseCase(
            setting_id=self.kwargs.get('setting_id')
        ).execute()