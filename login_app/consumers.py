import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class NumberConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = 'main_room'
        self.room_group_name = 'main_page_num_generator'

        async_to_sync(self.channel_layer.group_add)(
            'main_page_num_generator',
            self.channel_name
        )
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        number = text_data_json['message']
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
