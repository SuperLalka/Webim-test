import random
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from webim.celery import app


@app.task
def number_generator():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "main_page_num_generator",
        {
            "type": "number_message",
            "message": random.randint(0, 100)
        }
    )
