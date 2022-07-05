import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class NotificationConsumer(WebsocketConsumer):

    # connect to the websocket
    def connect(self):
        # Checking if the User is logged in
        if self.scope["user"].is_anonymous:
            # Reject the connection
            self.close()
        else:
            self.group_name = str(self.scope["user"].user_type)
            async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
            self.accept()

    # disconnect the Socket
    def disconnect(self, close_code):
        self.close()

    # Notify
    def notify(self, event):
        self.send(text_data=json.dumps(event["text"]))


#
class PortalUserNotificationConsumer(NotificationConsumer):

    # connect to the websocket
    def connect(self):
        # Checking if the User is logged in
        if self.scope["user"].user_type != 'portal_user':
            # Reject the connection
            print("*********************portel user")
            self.close()
        else:
            self.group_name = 'portal_user'
            async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
            self.accept()


class ConsultancyUserNotificationConsumer(NotificationConsumer):

    # connect to the websocket
    def connect(self):
        # Checking if the User is logged in
        if self.scope["user"].user_type != 'consultancy_user':
            # Reject the connection
            self.close()
        else:
            self.group_name = 'consultancy_user'
            async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
            self.accept()
#
#
# class StudentUserNotificationConsumer(NotificationConsumer):
#
#     # connect to the websocket
#     def connect(self):
#         # Checking if the User is logged in
#         if self.scope["user"].user_type != 'student_user':
#             # Reject the connection
#             self.close()
#         else:
#             self.group_name = 'student_user_notification_group'
#             async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
#             self.accept()
