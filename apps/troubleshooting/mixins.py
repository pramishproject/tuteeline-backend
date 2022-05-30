from apps.troubleshooting.usecases import GetTroubleshootUseCase


class TroubleshootMixin:
    def get_troubleshoot(self):
        return GetTroubleshootUseCase(troubleshoot_id=self.kwargs.get('troubleshoot_id')).execute()
