from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class NotificationMixin:
    notification_group = None
    notification_data = None

    def send_notification(self, data=None):
        channel_layer = get_channel_layer()
        groups = self.get_notification_group()
        for group in groups:
            async_to_sync(channel_layer.group_send)(
                group,
                {
                    "type": "notify",
                    "text": data if data else self.get_notification_data(),
                },
            )

    def get_notification_data(self):
        assert self.notification_data is not None, (
                "'%s' should either include a `notification_data` attribute, "
                "or override the `get_notification_data()` method."
                % self.__class__.__name__
        )
        return self.notification_data

    def get_notification_group(self):
        assert self.notification_group is not None, (
                "'%s' should either include a `notification_group` attribute, "
                "or override the `get_notification_group()` method."
                % self.__class__.__name__
        )
        return self.notification_group
