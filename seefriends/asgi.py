"""
ASGI config for seefriends project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import messagesapp.routing
import users.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seefriends.settings')

application = ProtocolTypeRouter({
   'http': get_asgi_application(),
   'websocket': AuthMiddlewareStack(
      URLRouter(
         messagesapp.routing.websocket_urlpatterns + users.routing.websocket_urlpatterns
      )
   )
})
