from django.urls import path, re_path
from . import consumers

# create your channel routings here

websocket_urlpatterns = [
   path('ws/message/<str:pk>/', consumers.ChatConsumer.as_asgi())
]