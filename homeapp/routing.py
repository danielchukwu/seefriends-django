from django.urls import path
from homeapp import consumers

# create your routings here

websocket_urlpatterns = [
   path('ws/likepost/<str:pk>/', consumers.LikePostConsumer.as_asgi()),
   path('ws/liketell/<str:pk>/', consumers.LikeTellConsumer.as_asgi()),
]