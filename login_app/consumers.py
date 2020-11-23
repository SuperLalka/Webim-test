import json
import redis
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class NumberConsumer(WebsocketConsumer):

    def websocket_connect(self, message):
        """
        Sends the current value of the generated number when opening a new socket
        """
        super().websocket_connect(self)
        connector = redis.Redis()
        number = connector.get('number').decode("utf-8")
        self.send(text_data=json.dumps({
            'event': 'Send',
            'message': number
        }))

    def connect(self):
        """
        Defines a new instance of a class with a single group
        """
        self.room_name = 'main_room'
        self.room_group_name = 'main_page_num_generator'

        async_to_sync(self.channel_layer.group_add)(
            'main_page_num_generator',
            self.channel_name
        )
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        """
        Listens to messages sent from the task manager
        """
        data = json.loads(text_data)
        number = data['message']
        async_to_sync(self.channel_layer.group_send)(
            'main_page_num_generator',
            {
                'type': 'number_message',
                'message': number
            }
        )

    def number_message(self, event):
        number = event['message']
        self.send(text_data=json.dumps({
            'event': 'Send',
            'message': number
        }))
