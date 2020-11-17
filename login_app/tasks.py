import random
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from webim.celery import app


MIN_NUMBER = 10000
MAX_NUMBER = 99999


@app.task
def number_generator():
    """
    A task for the task manager that
    sends a message to a single group
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "main_page_num_generator",
        {
            "type": "number_message",
            "message": random.randint(MIN_NUMBER, MAX_NUMBER)
        }
    )
