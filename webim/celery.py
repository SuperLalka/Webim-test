import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webim.settings')

app = Celery('webim')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'number-generator-every-5-seconds': {
        'task': 'login_app.tasks.number_generator',
        'schedule': 5.0,
    }
}
