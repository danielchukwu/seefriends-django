from django.urls import path, re_path
from . import consumers

# create your channel routings here

websocket_urlpatterns = [
   path('ws/message/<str:pk>/', consumers.ChatConsumer.as_asgi()),
   path('ws/message/<str:pk1>/<str:pk2>/', consumers.ChatConsumerForReact.as_asgi()), # pk: is for whom you want to chat with and | pk2: is for you 
]