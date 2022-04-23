from django.urls import path, re_path
from . import consumers

# create your channel routings here

websocket_urlpatterns = [
   path('ws/online/', consumers.OnlineConsumer.as_asgi()),
]