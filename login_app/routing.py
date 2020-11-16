from django.conf.urls import url

from login_app import consumers


websocket_urlpatterns = [
    url(r'ws/index$', consumers.NumberConsumer.as_asgi()),
]
