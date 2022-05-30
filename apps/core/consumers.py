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
            self.group_name = str(self.scope["user"].pk)
            async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
            self.accept()

    # disconnect the Socket
    def disconnect(self, close_code):
        self.close()
        # pass

    # Notify
    def notify(self, event):
        self.send(text_data=json.dumps(event["text"]))
